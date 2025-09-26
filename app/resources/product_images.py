import os
import time

from models import db, ShopModel, ProductImagesModel, ProductsModel
from flask_restful import Resource
from flask import request
from werkzeug.utils import secure_filename

from common.validators import validate_shop, validate_product
from common.config import UPLOAD_FOLDER, UPLOAD_FOLDER_NAME
from wrappers.permissions import shop_owner_permissions
from sqlalchemy import desc


class ProductImages(Resource):
    def get(self):
        try:
            shop_id = request.args.get("shop_id")
            shop, err = validate_shop(shop_id=shop_id)

            if err:
                return err

            product_id = request.args.get("product_id")
            product, err = validate_product(product_id=product_id, shop_id=shop.id)

            if err:
                return err

            images = ProductImagesModel.query.filter_by(
                shop_id=shop.id, product_id=product.id
            )

            return [image.to_dict() for image in images]

        except Exception as e:
            return f"something went wrong: {e}", 500

    @shop_owner_permissions()
    def post(self, user):
        try:
            shop_id = request.args.get("shop_id")
            shop, err = validate_shop(shop_id=shop_id)

            if err:
                return err

            product_id = request.args.get("product_id")
            product, err = validate_product(product_id=product_id, shop_id=shop.id)

            if err:
                return err

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
                    timestamp = time.time()
                    ext = os.path.splitext(image.filename)[1]
                    filename = secure_filename(f"{timestamp}{ext}")
                    save_path = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(save_path)

                    product_image = ProductImagesModel(
                        product_id=product.id,
                        path=f"/{UPLOAD_FOLDER_NAME}/{filename}",
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
    def delete(self, user):
        try:
            shop_id = request.args.get("shop_id")
            shop, err = validate_shop(shop_id=shop_id)

            if err:
                return err

            product_id = request.args.get("product_id")
            product, err = validate_product(product_id=product_id, shop_id=shop.id)

            if err:
                return err

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

                    if os.path.exists(os.path.join(UPLOAD_FOLDER, image.filename)):
                        os.remove(os.path.join(UPLOAD_FOLDER, image.filename))

            if image_id:
                image = ProductImagesModel.query.filter_by(
                    shop_id=shop.id, product_id=product.id, id=image_id
                ).first()

                if not image:
                    return "no image", 404

                db.session.delete(image)
                if os.path.exists(os.path.join(UPLOAD_FOLDER, image.filename)):
                    os.remove(os.path.join(UPLOAD_FOLDER, image.filename))

            db.session.commit()

            return "ok", 204

        except Exception as e:
            return f"something went wrong: {e}", 500
