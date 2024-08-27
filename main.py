import time

from src.csv_saver import csv_saver
from src.products import Products

products = Products.cast_to_object_list()

products_list = []
for product in products:
    product.get_more_information_about_products()
    products_list.append({
        "name": product.name,
        "rating": product.rating,
        "price": product.price,
        "url": product.url,
        "description": product.description,
        "instruction": product.instruction,
        "country": product.country
    })
    print(f'{product.url} - DONE')
    time.sleep(0.1)

csv_saver(products_list, 'result/products.csv')
