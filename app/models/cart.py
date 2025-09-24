from sqlalchemy import UniqueConstraint
from . import db, ProductsModel


class CartModel(db.Model):
    __tablename__ = "carts"

    __table_args__ = (UniqueConstraint("user_id"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=True)

    items = db.relationship(
        "CartItemModel",
        foreign_keys="CartItemModel.cart_id",
        backref="cart",
    )

    @property
    def total(self):
        return sum(item.total for item in self.items if item.total)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "shop_id": self.shop_id,
            "items": [item.to_dict() for item in self.items],
            "total": self.total,
        }


class CartItemModel(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    product = db.relationship(ProductsModel, foreign_keys=[product_id])

    @property
    def total(self):
        if self.product and hasattr(self.product, "price"):
            return self.product.price * self.quantity
        return 0

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.to_dict() if self.product else None,
            "quantity": self.quantity,
            "total": self.total,
        }
