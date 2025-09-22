from flask import request
from flask_restful import Resource
from models import ProductsModel, db
from wrappers import shop_required, validate_shop


class ProductsList(Resource):
    @validate_shop()
    def get(self, shop_id):
        try:
            products = ProductsModel.query.filter_by(shop_id=shop_id)

            return [product.to_dict() for product in products]

        except Exception as e:
            return f"something went wrong: {e}"

    @shop_required()
    @validate_shop()
    def post(self, shop_id, user):
        try:
            data = request.get_json()

            name = data.get("name", "").strip()
            price = data.get("price", 0)

            if name is None or len(name) == 0:
                return "name is missing", 500

            if price is None or int(price) == 0:
                return "price is missing", 500

            new_product = ProductsModel(
                name=name, price=price, user_id=user.id, shop_id=shop_id
            )
            db.session.add(new_product)
            db.session.commit()

            return new_product.to_dict(), 201

        except Exception:
            return "something went wrong", 500


class Product(Resource):
    @validate_shop()
    def get(self, product_id, shop_id):
        try:
            product = ProductsModel.query.filter_by(
                id=product_id, shop_id=shop_id
            ).first()

            if not product:
                return "product not found", 404

            return product.to_dict()

        except Exception as e:
            return f"something went wrong: {e}", 500

    @shop_required()
    @validate_shop()
    def put(self, product_id, shop_id, user):
        try:
            data = request.get_json()

            product = ProductsModel.query.filter_by(
                id=product_id, shop_id=shop_id, user_id=user.id
            ).first()

            if not product:
                return "product not found"

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

    @shop_required()
    @validate_shop()
    def delete(self, shop_id, product_id, user):
        try:
            product = ProductsModel.query.filter_by(
                id=product_id, shop_id=shop_id, user_id=user.id
            ).first()

            if not product:
                return "shop not found", 404

            db.session.delete(product)
            db.session.commit()

            return "ok", 200

        except Exception as e:
            return "something went wrong", 500
