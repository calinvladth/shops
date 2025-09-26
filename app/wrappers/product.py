from functools import wraps
from models import ProductsModel


def product_check(permissions="w"):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            product_id = kwargs.get("product_id")

            if not product_id:
                return "missing product", 500

            if permissions == "r":
                product = ProductsModel.query.get(product_id)

            if permissions == "w":
                user = kwargs.get("user")

                if not user:
                    return "user is missing", 500

                shop = kwargs.get("shop")

                if not shop:
                    return "shop is missing", 500

                product = ProductsModel.query.filter_by(
                    id=product_id, shop_id=shop.id, user_id=user.id
                ).first()

            if not product:
                return "product not found", 404

            return fn(product=product, *args, **kwargs)

        return decorator

    return wrapper
