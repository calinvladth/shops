from models import db, ProductImagesModel
from flask_restful import Resource
from flask import request

from wrappers import shop_owner_permissions, shop_check, product_check
from sqlalchemy import desc

from services import save_file, remove_file


class ProductImages(Resource):
    @shop_check("r")
    @product_check("r")
    def get(self, shop, product, **kwargs):
        try:
            images = ProductImagesModel.query.filter_by(
                shop_id=shop.id, product_id=product.id
            )

            return [image.to_dict() for image in images]

        except Exception as e:
            return f"something went wrong: {e}", 500

    @shop_owner_permissions()
    @shop_check("w")
    @product_check("w")
    def post(self, shop, product, user, **kwargs):
        try:
            last_image = (
                ProductImagesModel.query.filter_by(
                    shop_id=shop.id, product_id=product.id
                )
                .order_by(desc(ProductImagesModel.order))
                .first()
            )

            images = request.files.getlist("images")

            for index, image in enumerate(images):
                if image:
                    filename, url_path = save_file(image)

                    product_image = ProductImagesModel(
                        product_id=product.id,
                        path=url_path,
                        filename=filename,
                        shop_id=shop.id,
                        user_id=user.id,
                        order=(index + last_image.order + 1) if last_image else index,
                    )

                    db.session.add(product_image)

            db.session.commit()

            return "ok", 201

        except Exception as e:
            return f"something went wrong: {e}", 500

    @shop_owner_permissions()
    @shop_check("w")
    @product_check("w")
    def delete(self, shop, product, **kwargs):
        try:
            image_id = request.args.get("image_id")
            all = request.args.get("all")

            if not image_id and all == "true":
                images = ProductImagesModel.query.filter_by(
                    shop_id=shop.id, product_id=product.id
                )

                if not images:
                    return "no images", 404

                for image in images:
                    db.session.delete(image)
                    remove_file(image)

            if image_id:
                image = ProductImagesModel.query.filter_by(
                    shop_id=shop.id, product_id=product.id, id=image_id
                ).first()

                if not image:
                    return "no image", 404

                db.session.delete(image)
                remove_file(image)

            db.session.commit()

            return "ok", 204

        except Exception as e:
            return f"something went wrong: {e}", 500
