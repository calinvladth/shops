from flask import request
from flask_restful import Resource
from models import CartModel, CartItemModel, ProductsModel, ShopModel, db
from wrappers import (
    auth_required,
    validate_shop,
)


class CartList(Resource):
    @auth_required()
    def get(self, user):
        try:
            cart = CartModel.query.filter_by(user_id=user.id).first()

            if not cart:
                cart = CartModel(user_id=user.id)
                db.session.add(cart)
                db.session.commit()

            return cart.to_dict()

        except Exception as e:
            return f"something went wrong: {e}", 500


class CartItems(Resource):
    @auth_required()
    def post(self, user):
        try:
            data = request.get_json()

            shop_id = data.get("shop_id")
            product_id = data.get("product_id")

            if not shop_id:
                return "shop is missing", 500

            if not product_id:
                return "product is missing", 500

            cart = CartModel.query.filter_by(user_id=user.id).first()

            if not cart:
                return "cart doesn't exist", 404

            shop = ShopModel.query.get(shop_id)

            if not shop:
                return "shop doesn't exist", 404

            product = ProductsModel.query.get(product_id)

            if not product:
                return "product doesn't exist", 404

            if shop_id != product.shop_id:
                return "product is from another shop", 500

            if cart.shop_id != product.shop_id:
                cart.shop_id = product.shop_id

                cart_items = CartItemModel.query.filter_by(user_id=user.id).all()
                for item in cart_items:
                    db.session.delete(item)

            is_cart_item = CartItemModel.query.filter_by(product_id=product_id).first()

            if is_cart_item:
                return "product is already in cart", 500

            new_cart_item = CartItemModel(
                user_id=user.id,
                shop_id=shop_id,
                product_id=product.id,
                cart_id=cart.id,
            )

            db.session.add(new_cart_item)
            db.session.commit()

            return "ok", 200

        except Exception as e:
            return f"something went wrong: {e}", 500

    @auth_required()
    def delete(self, user):
        try:
            data = request.get_json()
            cart_item_id = data.get("cart_item")

            if not cart_item_id:
                return "cart item is missing", 500

            cart_item = CartItemModel.query.filter_by(
                id=cart_item_id, user_id=user.id
            ).first()

            if not cart_item:
                return "cart item doesn't exist", 404

            db.session.delete(cart_item)
            db.session.commit()

            return "ok", 200

        except Exception as e:
            return f"something went wrong: {e}", 500


class CartItemUpdate(Resource):
    @auth_required()
    def put(self, user, cart_item_id):
        return f"update cart item {cart_item_id}", 200
