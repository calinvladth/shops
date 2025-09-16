from flask import request
from flask_restful import Resource
from models import CartModel, CartItemModel, db
from wrappers import (
    auth_required,
    validate_product,
    validate_shop,
    validate_cart,
)


# Get or create cart
class CartList(Resource):
    @auth_required()
    def get(self, user):
        cart = CartModel.query.filter_by(user_id=user.id).first()

        if not cart:
            cart = CartModel(user_id=user.id)
            db.session.add(cart)
            db.session.commit()

        cart_items = CartItemModel.query.filter_by(cart_id=cart.id)

        return {
            "cart": cart.to_dict(),
            "products": [item.to_dict() for item in cart_items],
        }


class CartItems(Resource):
    @auth_required()
    def get(self, user, shop_id):
        cart_items = CartItemModel.query.filter_by(user_id=user.id, shop_id=shop_id)

        return [item.to_dict() for item in cart_items]

    @auth_required()
    @validate_shop()
    @validate_product()
    @validate_cart()
    def post(self, user, shop_id):
        data = request.get_json()

        if not data["cart_id"]:
            return "cart is missing", 500

        if not data["product_id"]:
            return "product is missing", 500

        new_cart_item = CartItemModel(
            user_id=user.id,
            shop_id=shop_id,
            product_id=data["product_id"],
            cart_id=data["cart_id"],
        )

        db.session.add(new_cart_item)
        db.session.commit()

        return "ok", 200

    @auth_required()
    def delete(self, user, product_id):
        cart_item = CartItemModel.query.filter_by(
            user_id=user.id, product_id=product_id
        ).first()

        if not cart_item:
            return f"product {product_id} is missing from cart"

        db.session.delete(cart_item)
        db.session.commit()

        return "ok", 200
