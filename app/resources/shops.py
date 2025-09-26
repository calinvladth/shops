from flask import request
from flask_restful import Resource
from models import ShopModel, db
from wrappers import shop_owner_permissions, shop_check


class ShopList(Resource):
    def get(self):
        try:
            shops = ShopModel.query.all()

            return [shop.to_dict() for shop in shops]

        except Exception as e:
            return f"something went wrong: {e}", 500

    @shop_owner_permissions()
    def post(self, user):
        try:
            data = request.get_json()
            name = data.get("name", "").strip()
            address = data.get("address", "").strip()
            city = data.get("city", "").strip()
            latitude = data.get("latitude", 0)
            longitude = data.get("longitude", 0)

            if not name or len(name) == 0:
                return "name is missing", 500

            if not address or len(address) == 0:
                return "address is missing", 500

            if not city or len(city) == 0:
                return "city is missing", 500

            if not latitude:
                return "latitude is missing", 500

            if not longitude:
                return "longitude is missing", 500

            new_shop = ShopModel(
                name=name,
                address=address,
                city=city,
                latitude=latitude,
                longitude=longitude,
                user_id=user.id,
            )
            db.session.add(new_shop)
            db.session.commit()

            return new_shop.to_dict(), 201

        except Exception as e:
            return f"something went wrong: {e}", 500


class ShopResource(Resource):
    def get(self, shop_id):
        try:
            shop = ShopModel.query.get(shop_id)

            if not shop:
                return "shop not found", 404

            return shop.to_dict()

        except Exception as e:
            return f"something went wrong: {e}", 500

    @shop_owner_permissions()
    @shop_check()
    def put(self, shop, **kwargs):
        try:
            print(shop)
            data = request.get_json()
            name = data.get("name", "").strip()
            address = data.get("address", "").strip()
            city = data.get("city", "").strip()
            latitude = data.get("latitude", 0)
            longitude = data.get("longitude", 0)

            if name:
                shop.name = name

            if address:
                shop.address = address

            if city:
                shop.city = city

            if latitude:
                shop.latitude = latitude

            if longitude:
                shop.longitude = longitude

            db.session.commit()

            return shop.to_dict()

        except Exception as e:
            return "something went wrong", 500

    @shop_owner_permissions()
    @shop_check()
    def delete(self, shop, **kwargs):
        try:
            print(shop)
            db.session.delete(shop)
            db.session.commit()

            return "ok", 200

        except Exception as e:
            return f"something went wrong: {e}", 500
