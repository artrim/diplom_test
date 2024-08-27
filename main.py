from src.csv_saver import csv_saver
from src.try_oop import Products

products = Products.cast_to_object_list()

products_list = []
for product in products:
    product.get_other_information_about_products()
    products_list.append({
        "name": product.name,
        "rating": product.rating,
        "price": product.price,
        "url": product.url,
        "description": product.description,
        "instruction": product.instruction,
        "country": product.country
    })

csv_saver(products_list, 'result/test_products_2.csv')
