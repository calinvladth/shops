from functools import wraps

from models import ShopModel, CartModel
from flask import request


def shop_check(permissions="w"):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):

            shop_id = kwargs.get("shop_id", None) or request.args.get("shop_id")

            if not shop_id:
                return "missing shop", 500

            if permissions == "r":
                shop = ShopModel.query.filter_by(id=shop_id).first()

            if permissions == "w":
                user = kwargs.get("user")

                if not user:
                    return "user is missing"

                shop = ShopModel.query.filter_by(id=shop_id, user_id=user.id).first()

            if not shop:
                return "shop not found", 404

            return fn(shop=shop, *args, **kwargs)

        return decorator

    return wrapper


def validate_cart():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            cart_id = kwargs.get("cart_id", None)

            if not cart_id:
                return "missing cart", 500

            cart = CartModel.query.get(cart_id)

            if not cart:
                return "cart not found", 404

            return fn(*args, **kwargs)

        return decorator

    return wrapper
