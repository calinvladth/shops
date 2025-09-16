from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import ShopModel, ProductsModel, CartModel


def validate_shop():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            shop_id = kwargs.get("shop_id", None)

            if not shop_id:
                return "missing shop", 500

            shop = ShopModel.query.get(shop_id)

            if not shop:
                return "shop not found", 404

            return fn(*args, **kwargs)

        return decorator

    return wrapper


def validate_product():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            product_id = kwargs.get("product_id", None)
            print("PPP: ", args)

            if not product_id:
                return "missing product", 500

            product = ProductsModel.query.get(product_id)

            if not product:
                return "product not found", 404

            return fn(*args, **kwargs)

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
