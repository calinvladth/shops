from . import db


class ProductsModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    images = db.relationship(
        "ProductImagesModel",
        foreign_keys="ProductImagesModel.product_id",
        backref="image",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "shop_id": self.shop_id,
            "user_id": self.user_id,
            "images": [image.to_dict() for image in self.images],
        }


class ProductImagesModel(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    order = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "filename": self.filename,
            "order": self.order,
            # "shop_id": self.shop_id,
            # "user_id": self.user_id,
        }
