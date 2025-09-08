from flask import request
from flask_restful import Resource
from models import ProductsModel, db
from wrappers import shop_required, validate_shop


class ProductsList(Resource):
    @validate_shop()
    def get(self, shop_id):
        products = ProductsModel.query.filter_by(shop_id=shop_id)

        return [product.to_dict() for product in products]

    @shop_required()
    @validate_shop()
    def post(self, shop_id, user):
        data = request.get_json()
        new_product = ProductsModel(name=data["name"], user_id=user.id, shop_id=shop_id)
        db.session.add(new_product)
        db.session.commit()

        return new_product.to_dict(), 201


class Product(Resource):
    @validate_shop()
    def get(self, product_id, shop_id):
        product = ProductsModel.query.filter_by(id=product_id, shop_id=shop_id).first()

        if not product:
            return "product not found", 404

        return product.to_dict()

    @shop_required()
    @validate_shop()
    def put(self, product_id, shop_id, user):
        data = request.get_json()
        product = ProductsModel.query.filter_by(
            id=product_id, shop_id=shop_id, user_id=user.id
        ).first()

        if not product:
            return "product not found"

        product.name = data["name"]
        db.session.commit()

        return product.to_dict()

    @shop_required()
    @validate_shop()
    def delete(self, shop_id, product_id, user):
        product = ProductsModel.query.filter_by(
            id=product_id, shop_id=shop_id, user_id=user.id
        ).first()

        if not product:
            return "shop not found", 404

        db.session.delete(product)
        db.session.commit()

        return "ok", 200
