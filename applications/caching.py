from flask import current_app as app
from flask_caching import Cache
from .model import *

cache = Cache()


@cache.memoize(30)
def get_categories():
    categories = Categories.query.all()
    return categories


@cache.memoize(30)
def get_product(product_id):
    product = Product.query.get(product_id)
    return product
