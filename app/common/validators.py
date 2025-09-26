from models import ShopModel, ProductsModel


def validate_shop(shop_id):
    if not shop_id:
        return None, ("shop id is missing", 400)

    shop = ShopModel.query.get(shop_id)
    if not shop:
        return None, ("shop not found", 404)

    return shop, None


def validate_product(product_id, shop_id):
    if not product_id:
        return None, ("product id is missing", 500)

    product = ProductsModel.query.filter_by(id=product_id, shop_id=shop_id).first()

    if not product:
        return "product not found", 404

    return product, None
