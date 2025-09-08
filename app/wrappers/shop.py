from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import ShopModel


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
