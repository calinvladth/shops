from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

from .users import UserModel
from .shops import ShopModel
from .products import ProductsModel, ProductImagesModel
from .cart import CartModel, CartItemModel
from .order import OrderModel, OrderItemModel, OrderStatus
