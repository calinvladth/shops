import os
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from common.config import UPLOAD_FOLDER, CWD
from resources.file_uploader import FileUploader

from resources.shop import Shop
from resources.shop_menu import ShopMenu
from models import db, jwt

from resources import (
    ForgotPassword,
    Login,
    RegisterUser,
    RegisterShop,
    ResetPassword,
    RestrictedRoute,
    ShopList,
    ShopResource,
    ProductsList,
    Product,
    CartList,
    CartItems,
)


app = Flask(
    __name__,
    static_folder=os.path.join(CWD, UPLOAD_FOLDER),
)

# Configuration
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "whatever"


# Init database
db.init_app(app)
jwt.init_app(app)

app.config["UPLOAD_FOLDER"] = os.path.join(CWD, UPLOAD_FOLDER)
api = Api(app)


api.add_resource(FileUploader, "/upload")
api.add_resource(Shop, "/shop")
api.add_resource(ShopMenu, "/shop/<shop_id>")

api.add_resource(RegisterUser, "/register-user")
api.add_resource(RegisterShop, "/register-shop")
api.add_resource(Login, "/login")
api.add_resource(ForgotPassword, "/forgot-password")
api.add_resource(ResetPassword, "/reset-password")
api.add_resource(RestrictedRoute, "/restricted")

api.add_resource(ShopList, "/shops")
api.add_resource(ShopResource, "/shops/<int:shop_id>")
api.add_resource(ProductsList, "/shops/<int:shop_id>/products")
api.add_resource(Product, "/shops/<int:shop_id>/products/<int:product_id>")

api.add_resource(CartList, "/cart")
api.add_resource(CartItems, "/cart/<int:shop_id>")


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    with app.app_context():
        db.create_all()

    app.run(port=8000, debug=True)
