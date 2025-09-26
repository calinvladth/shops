from flask import request
from flask_restful import Resource
from models import ProductsModel, db, CartItemModel
from wrappers import shop_owner_permissions, shop_check, product_check


class ProductsList(Resource):
    @shop_check("r")
    def get(self, shop, **kwargs):
        try:
            products = ProductsModel.query.filter_by(shop_id=shop.id)

            return [product.to_dict() for product in products]

        except Exception as e:
            return f"something went wrong: {e}"

    @shop_owner_permissions()
    @shop_check("w")
    def post(self, user, shop, **kwargs):
        try:
            data = request.get_json()

            name = data.get("name", "").strip()
            price = data.get("price", 0)

            if not name or len(name) == 0:
                return "name is missing", 500

            if not price or int(price) == 0:
                return "price is missing", 500

            new_product = ProductsModel(
                name=name, price=price, shop_id=shop.id, user_id=user.id
            )
            db.session.add(new_product)
            db.session.commit()

            return new_product.to_dict(), 201

        except Exception:
            return "something went wrong", 500


class Product(Resource):
    @shop_check("r")
    @product_check("r")
    def get(self, product, **kwargs):

        try:
            return product.to_dict()

        except Exception as e:
            return f"something went wrong: {e}", 500

    @shop_owner_permissions()
    @shop_check("w")
    @product_check("w")
    def put(self, product, **kwargs):
        try:
            data = request.get_json()

            name = data.get("name", "").strip()
            price = data.get("price", 0)

            if name:
                product.name = name

            if price and int(price) > 0:
                product.price = price

            db.session.commit()

            return product.to_dict()

        except Exception as e:
            return f"something went wrong: {e}", 500

    @shop_owner_permissions()
    @shop_check("w")
    @product_check("w")
    def delete(self, product, **kwargs):
        try:
            cart_items = CartItemModel.query.filter_by(product_id=product.id)

            for item in cart_items:
                db.session.delete(item)

            db.session.delete(product)
            db.session.commit()

            return "ok", 200

        except Exception as e:
            return f"something went wrong: {e}", 500
