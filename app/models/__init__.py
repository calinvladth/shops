from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


# @jwt.unauthorized_loader
# def unauthorized_response(*args, **kwargs):
#     return {"message": "Missing Authorization Header"}, 401


# @jwt.invalid_token_loader
# def invalid_token_response(*args, **kwargs):
#     return {"message": "Invalid token"}, 422


# @jwt.expired_token_loader
# def expired_token_response(*args, **kwargs):
#     return {"message": "Token has expired"}, 401


# @jwt.revoked_token_loader
# def revoked_token_response(*args, **kwargs):
#     return {"message": "Token has been revoked"}, 401


# Import models here so they register with SQLAlchemy
from .todo import TodoModel
from .shops import ShopModel
from .products import ProductsModel
