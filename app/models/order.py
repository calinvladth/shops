from sqlalchemy import Enum
from . import db
import enum


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=True)
    status = db.Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total = db.Column(db.Float, nullable=False, default=0.0)

    items = db.relationship(
        "OrderItemModel",
        foreign_keys="OrderItemModel.order_id",
        backref="order",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "shop_id": self.shop_id,
            "status": self.status.value,
            "total": self.total,
            "items": [item.to_dict() for item in self.items],
        }

    # TODO: Move this logic to resources
    @classmethod
    def from_cart(cls, cart):
        order = cls(
            user_id=cart.user_id,
            shop_id=cart.shop_id,
            total=cart.total,
        )

        for cart_item in cart.items:
            order_item = OrderItemModel(
                product_id=cart_item.product_id,
                product_name=cart_item.product.name if cart_item.product else None,
                unit_price=cart_item.product.price if cart_item.product else 0,
                quantity=cart_item.quantity,
                total=cart_item.total,
                shop_id=cart_item.shop_id,
            )
            order.items.append(order_item)

        return order


class OrderItemModel(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total = db.Column(db.Float, nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "unit_price": self.unit_price,
            "quantity": self.quantity,
            "total": self.total,
        }
