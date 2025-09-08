from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import ProductsModel, db


class ProductsList(Resource):
    def get(self, shop_id):
        products = ProductsModel.query.filter_by(shop_id=shop_id)

        return [product.to_dict() for product in products]

    @jwt_required()
    def post(self, shop_id):
        user_id = get_jwt_identity()

        data = request.get_json()
        new_product = ProductsModel(name=data["name"], user_id=user_id, shop_id=shop_id)
        db.session.add(new_product)
        db.session.commit()

        return new_product.to_dict(), 201


class Product(Resource):
    def get(self, product_id, shop_id):
        product = ProductsModel.query.filter_by(id=product_id, shop_id=shop_id).first()

        if not product:
            return "product not found", 404

        return product.to_dict()

    @jwt_required()
    def put(self, product_id, shop_id):
        user_id = get_jwt_identity()
        data = request.get_json()
        product = ProductsModel.query.filter_by(
            id=product_id, shop_id=shop_id, user_id=user_id
        ).first()

        if not product:
            return "product not found"

        product.name = data["name"]
        db.session.commit()

        return product.to_dict()

    @jwt_required()
    def delete(self, shop_id, product_id):
        user_id = get_jwt_identity()
        product = ProductsModel.query.filter_by(
            id=product_id, shop_id=shop_id, user_id=user_id
        ).first()

        if not product:
            return "shop not found", 404

        db.session.delete(product)
        db.session.commit()

        return "ok", 200
