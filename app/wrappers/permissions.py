from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import UserModel


def auth_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()

            user_id = get_jwt_identity()
            user = UserModel.query.get(user_id)

            if not user:
                return "unauthorized", 403

            return fn(user=user, *args, **kwargs)

        return decorator

    return wrapper


def shop_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()

            user_id = get_jwt_identity()
            user = UserModel.query.get(user_id)

            if not user:
                return "unauthorized", 403

            if not user.is_shop:
                return "unauthorized", 403

            return fn(user=user, *args, **kwargs)

        return decorator

    return wrapper
