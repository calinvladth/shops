from flask import request
from flask_restful import Resource
from models import CartModel, CartItemModel, ProductsModel, db
from wrappers import (
    auth_required,
    validate_shop,
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

        return cart.to_dict()


class CartItems(Resource):
    @auth_required()
    def get(self, user, shop_id):
        cart_items = CartItemModel.query.filter_by(user_id=user.id, shop_id=shop_id)

        return [item.to_dict() for item in cart_items]

    @auth_required()
    @validate_shop()
    def post(self, user, shop_id):
        data = request.get_json()

        if not data["product_id"]:
            return "product is missing", 500

        cart = CartModel.query.filter_by(user_id=user.id).first()
        product = ProductsModel.query.get(data["product_id"])

        if cart.shop_id != product.shop_id:
            cart.shop_id = product.shop_id

            cart_items = CartItemModel.query.filter_by(user_id=user.id).all()
            for item in cart_items:
                db.session.delete(item)

        new_cart_item = CartItemModel(
            user_id=user.id,
            shop_id=shop_id,
            product_id=product.id,
            cart_id=cart.id,
        )

        db.session.add(new_cart_item)
        db.session.commit()

        return "ok", 200

    @auth_required()
    @validate_shop()
    def delete(self, user, shop_id):
        data = request.get_json()
        cart_item = CartItemModel.query.filter_by(
            user_id=user.id, product_id=data["product_id"]
        ).first()

        if not cart_item:
            return f"product {data["product_id"]} is missing from cart"

        db.session.delete(cart_item)
        db.session.commit()

        return "ok", 200
