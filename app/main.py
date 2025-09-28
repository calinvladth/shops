import os
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from common.config import UPLOAD_FOLDER, CWD

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
    ProductImages,
    OrderList,
    OrderResource,
    OrderAdminResource,
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


# Authentication
api.add_resource(RegisterUser, "/register-user")
api.add_resource(RegisterShop, "/register-shop")
api.add_resource(Login, "/login")
api.add_resource(ForgotPassword, "/forgot-password")
api.add_resource(ResetPassword, "/reset-password")
api.add_resource(RestrictedRoute, "/restricted")

# Shops
api.add_resource(ShopList, "/shops")
api.add_resource(ShopResource, "/shops/<int:shop_id>")

# Products
api.add_resource(ProductsList, "/products")
api.add_resource(Product, "/products/<int:product_id>")
api.add_resource(ProductImages, "/product-images")

# Cart
api.add_resource(CartList, "/cart")
api.add_resource(CartItems, "/cart_item")

# Orders
api.add_resource(OrderList, "/orders")
api.add_resource(OrderResource, "/orders/<int:order_id>")
api.add_resource(OrderAdminResource, "/shop/orders", "/shop/orders/<int:order_id>")


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    with app.app_context():
        db.create_all()

    app.run(port=8000, debug=True)
