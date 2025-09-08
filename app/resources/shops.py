from flask import request
from flask_restful import Resource
from models import ShopModel, db
from wrappers import shop_required


class ShopList(Resource):
    def get(self):
        shops = ShopModel.query.all()

        return [shop.to_dict() for shop in shops]

    @shop_required()
    def post(self, user):
        data = request.get_json()
        new_shop = ShopModel(title=data["title"], user_id=user.id)
        db.session.add(new_shop)
        db.session.commit()

        return new_shop.to_dict(), 201


class ShopResource(Resource):
    def get(self, shop_id):
        shop = ShopModel.query.get(shop_id)

        if not shop:
            return "shop not found", 404

        return shop.to_dict()

    @shop_required()
    def put(self, shop_id, user):
        data = request.get_json()
        shop = ShopModel.query.filter_by(id=shop_id, user_id=user.id).first()

        if not shop:
            return "shop not found"

        shop.title = data["title"]
        db.session.commit()

        return shop.to_dict()

    @shop_required()
    def delete(self, shop_id, user):
        shop = ShopModel.query.filter_by(id=shop_id, user_id=user.id).first()

        if not shop:
            return "shop not found", 404

        db.session.delete(shop)
        db.session.commit()

        return "ok", 200
