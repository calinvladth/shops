from flask_restful import Resource
from flask import request


class ShopMenu(Resource):
    def get(self, shop_id):
        data = f"Get menu {shop_id}"
        return data

    def post(self, shop_id):
        body = request.get_json()
        if not "name" in body:
            return "name is missing", 500

        if not "price" in body:
            return "price is missing", 500

        if not "photos" in body:
            return "photos are missing", 500

        if not "others" in body:
            return "others are missing", 500

        return "Add menu"
