from flask import request
from flask_restful import Resource
from models import CartItemModel, db
from wrappers import (
    user_permissions,
    shop_check,
    product_check,
    cart_check,
    cart_item_check,
)


class CartList(Resource):
    @user_permissions()
    @cart_check()
    def get(self, cart, **kwargs):
        try:
            return cart.to_dict()

        except Exception as e:
            return f"something went wrong: {e}", 500


class CartItems(Resource):
    @user_permissions()
    @shop_check("r")
    @product_check("r")
    @cart_check()
    def post(self, shop, product, cart, user, **kwargs):
        try:
            if shop.id != product.shop_id:
                return "product is from another shop", 500

            if cart.shop_id != product.shop_id:
                cart.shop_id = product.shop_id

                cart_items = CartItemModel.query.filter_by(user_id=user.id).all()
                for item in cart_items:
                    db.session.delete(item)

            is_cart_item = CartItemModel.query.filter_by(product_id=product.id).first()

            if is_cart_item:
                return "product is already in cart", 500

            new_cart_item = CartItemModel(
                user_id=user.id,
                shop_id=shop.id,
                product_id=product.id,
                cart_id=cart.id,
            )

            db.session.add(new_cart_item)
            db.session.commit()

            return "ok", 200

        except Exception as e:
            return f"something went wrong: {e}", 500

    @user_permissions()
    @cart_item_check()
    def put(self, cart_item, **kwargs):
        try:
            data = request.get_json()

            quantity = data.get("quantity")

            if not quantity:
                return "quantity is missing", 500

            cart_item.quantity = quantity

            db.session.add(cart_item)
            db.session.commit()

            return "ok", 200

        except Exception as e:
            return f"something went wrong: {e}", 500

    @user_permissions()
    @cart_item_check()
    def delete(self, cart_item, **kwargs):
        try:
            db.session.delete(cart_item)
            db.session.commit()

            return "ok", 200

        except Exception as e:
            return f"something went wrong: {e}", 500
