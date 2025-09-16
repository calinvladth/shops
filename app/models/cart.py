from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from . import db


class CartModel(db.Model):
    __tablename__ = "carts"

    __table_args__ = (UniqueConstraint("user_id"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "shop_id": self.shop_id,
        }


class CartItemModel(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "shop_id": self.shop_id,
            "product_id": self.product_id,
        }
