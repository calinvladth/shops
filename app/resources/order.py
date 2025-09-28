from flask import request
from flask_restful import Resource
from models import db, OrderModel, OrderStatus, OrderItemModel
from wrappers import user_permissions, cart_check, shop_owner_permissions, shop_check


class OrderList(Resource):
    @user_permissions()
    def get(self, user, **kwargs):
        try:
            orders = OrderModel.query.filter_by(user_id=user.id).all()
            return [order.to_dict() for order in orders], 200

        except Exception as e:
            return f"something went wrong: {e}", 500

    @user_permissions()
    @cart_check()
    def post(self, cart, user, **kwargs):
        """Create a new order from the user's cart"""
        """
            TODO: Create order
            Add order items
            Remove cart items
            commit
        """
        try:
            if not cart.items or len(cart.items) == 0:
                return "cart is empty", 400

            order = OrderModel(
                user_id=cart.user_id, shop_id=cart.shop_id, total=cart.total
            )

            db.session.add(order)
            db.session.flush()

            for cart_item in cart.items:
                order_item = OrderItemModel(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    product_name=cart_item.product.name if cart_item.product else None,
                    unit_price=cart_item.product.price if cart_item.product else 0,
                    quantity=cart_item.quantity,
                    total=cart_item.total,
                    shop_id=cart_item.shop_id,
                )
                db.session.add(order_item)
                db.session.delete(cart_item)

            cart.shop_id = None
            db.session.commit()

            return order.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return f"something went wrong: {e}", 500


class OrderResource(Resource):
    @user_permissions()
    def get(self, order_id, user, **kwargs):
        try:
            order = OrderModel.query.filter_by(id=order_id, user_id=user.id).first()

            if not order:
                return "order not found", 404

            return order.to_dict(), 200

        except Exception as e:
            return f"something went wrong: {e}", 500


# TODO: Check on that
class OrderAdminResource(Resource):
    @shop_owner_permissions()
    @shop_check()
    def put(self, shop, order_id, **kwargs):
        try:
            order = OrderModel.query.filter_by(id=order_id, shop_id=shop.id).first()
            if not order:
                return "order not found", 404

            data = request.get_json()
            status = data.get("status")

            if not status or status not in OrderStatus:
                return "invalid status", 400

            new_status = OrderStatus(status)

            order.status = new_status
            db.session.add(order)
            db.session.commit()

            return order.to_dict(), 200

        except Exception as e:
            db.session.rollback()
            return f"something went wrong: {e}", 500

    @shop_owner_permissions()
    @shop_check("w")
    def get(self, shop, **kwargs):
        try:
            orders = OrderModel.query.filter_by(shop_id=shop.id).all()
            return [order.to_dict() for order in orders], 200

        except Exception as e:
            return f"something went wrong: {e}", 500
