from . import db


class ShopModel(db.Model):
    __tablename__ = "shops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(120), nullable=False)

    latitude = db.Column(db.Text, nullable=False)
    longitude = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "address": self.address,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


# class ShopImageModel(db.Model):
#     __tablename__ = "shop_image"

#     id = db.Column(db.Integer, primary_key=True)
#     shop_id = db.Column(
#         db.Integer, db.ForeignKey("shop.id"), nullable=False, unique=True
#     )
#     path = db.Column(db.String(255), nullable=False)
#     filename = db.Column(db.String(255), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "path": self.path,
#             "filename": self.filename,
#             "order": self.order,
#             # "shop_id": self.shop_id,
#             # "user_id": self.user_id,
#         }
