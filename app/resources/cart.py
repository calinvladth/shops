from flask import request
from flask_restful import Resource
from models import Cart, CartItem, db
from wrappers import shop_required, auth_required

# TODO: Much refactoring needed


class CartListResource(Resource):
    @auth_required()
    def get(self, user):
        cart = Cart.query.filter_by(user_id=user.id).first()

        if not cart:
            return "cart missing", 404

        cart_items = CartItem.query.filter_by(cart_id=cart.id)

        return {
            "cart": cart.to_dict(),
            "products": [item.to_dict() for item in cart_items],
        }

    @auth_required()
    def post(self, user):
        new_cart = Cart(user_id=user.id)
        db.session.add(new_cart)
        db.session.commit()

        return new_cart.to_dict(), 201


class CartItemResource(Resource):
    @auth_required()
    def get(self, user, product_id):
        cart_item = CartItem.query.filter_by(
            user_id=user.id, product_id=product_id
        ).first()

        if not cart_item:
            return f"product {product_id} is missing from cart"

        return cart_item.to_dict()

    @auth_required()
    def post(self, user, product_id):
        data = request.get_json()

        if not data["cart_id"]:
            return "cart is missing", 500

        if not data["shop_id"]:
            return "shop is missing", 500

        new_cart_item = CartItem(
            user_id=user.id,
            shop_id=data["shop_id"],
            product_id=product_id,
            cart_id=data["cart_id"],
        )

        db.session.add(new_cart_item)
        db.session.commit()

        return "ok", 200

    @auth_required()
    def delete(self, user, product_id):
        cart_item = CartItem.query.filter_by(
            user_id=user.id, product_id=product_id
        ).first()

        if not cart_item:
            return f"product {product_id} is missing from cart"

        db.session.delete(cart_item)
        db.session.commit()

        return "ok", 200


# class Product(Resource):
#     @validate_shop()
#     def get(self, product_id, shop_id):
#         product = ProductsModel.query.filter_by(id=product_id, shop_id=shop_id).first()

#         if not product:
#             return "product not found", 404

#         return product.to_dict()

#     @shop_required()
#     @validate_shop()
#     def put(self, product_id, shop_id, user):
#         data = request.get_json()
#         product = ProductsModel.query.filter_by(
#             id=product_id, shop_id=shop_id, user_id=user.id
#         ).first()

#         if not product:
#             return "product not found"

#         product.name = data["name"]
#         db.session.commit()

#         return product.to_dict()

#     @shop_required()
#     @validate_shop()
#     def delete(self, shop_id, product_id, user):
#         product = ProductsModel.query.filter_by(
#             id=product_id, shop_id=shop_id, user_id=user.id
#         ).first()

#         if not product:
#             return "shop not found", 404

#         db.session.delete(product)
#         db.session.commit()

#         return "ok", 200
