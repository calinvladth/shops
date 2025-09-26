from functools import wraps
from models import CartModel, db, CartItemModel
from flask import request


def cart_check():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = kwargs.get("user")

            if not user:
                return "user is missing", 500

            cart = CartModel.query.filter_by(user_id=user.id).first()

            if not cart:
                cart = CartModel(user_id=user.id)
                db.session.add(cart)
                db.session.commit()

            return fn(cart=cart, *args, **kwargs)

        return decorator

    return wrapper


def cart_item_check():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = kwargs.get("user")

            if not user:
                return "user is missing", 500

            cart_item_id = request.args.get("cart_item")
            if not cart_item_id:
                return "cart item is missing", 500

            cart_item = CartItemModel.query.filter_by(
                id=cart_item_id, user_id=user.id
            ).first()

            if not cart_item:
                return "item not found", 404

            return fn(cart_item=cart_item, *args, **kwargs)

        return decorator

    return wrapper
