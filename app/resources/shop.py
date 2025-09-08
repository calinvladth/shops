import os
from flask_restful import Resource
from flask import json, request
from common.config import UPLOAD_FOLDER


"""
    Shop should have:
    * name
    * location
    * address
    * user / somebody should create it
"""


class Shop(Resource):
    def get(self):
        user_id = request.args.get("user_id")
        path = os.path.join(UPLOAD_FOLDER, user_id, "data.json")
        if not os.path.exists(path):
            return "invalid user", 500

        file = json.load(open(os.path.join(path), "r"))
        print(file)

        return file

    def post(self):
        body = request.get_json()
        if "name" not in body:
            return "name is missing", 500

        if "location" not in body:
            return "location is missing", 500

        if "lat" and "lng" not in body["location"]:
            return "latitude and longitude are required", 500

        if "user_id" not in body:
            return "user is missing", 500

        if "address" not in body:
            return "address is missing", 500

        if "city" not in body["address"]:
            return "city is missing from address", 500

        if "country" not in body["address"]:
            return "country is missing from address", 500

        if "details" not in body["address"]:
            return "details are missing from address", 500

        path = os.path.join(UPLOAD_FOLDER, body["user_id"])
        if not os.path.exists(path):
            os.makedirs(path)

        file = open(os.path.join(path, "data.json"), "w+")
        json.dump(body, file)

        return "shop created", 200

    def put(self):
        return "Update shop"

    def delete(self):
        return "Delete shop"
