import pytest
from src.products import Products


@pytest.fixture
def product():
    return Products('Парфюмерная вода J.U.S Joyau Unique & Sensoriel  Sensoriel Ambraser',
                    '4.7',
                    '7 850',
                    'https://goldapple.ru/19000153561-sensoriel-ambraser')


def test_cast_to_object_list():
    products = Products.cast_to_object_list()
    assert products[0].name == 'Парфюмерная вода ESSENTIAL PARFUMS PARIS  Bois imperial refillable limited edition'


def test_product(product):
    assert product.name == 'Парфюмерная вода J.U.S Joyau Unique & Sensoriel  Sensoriel Ambraser'
    assert product.rating == '4.7'
    assert product.price == '7 850'
    assert product.url == 'https://goldapple.ru/19000153561-sensoriel-ambraser'


def test_get_other_information_about_products(product):
    product.get_more_information_about_products()
    assert product.description == ('Аромат J.U.S напоминает о летнем дне, проведенном на берегу моря: солнечные блики '
                                   'мерцают в воде, теплый песок ощущается на коже, морской бриз несет с собой свежесть'
                                   ', а время будто остановилось. Композиция передает контраст золотого и теплого '
                                   'сияния солнца и минеральной свежести морской соли. \nСогревающие ноты кедра и амбры '
                                   'делают композицию чувственной и уносят в беззаботные и расслабленные дни отдыха. '
                                   'Классификация аромата: соленый, амбровый. Парфюмер – Aurélien Guichard.\n\n')
    assert product.instruction == 'Для наружного применения.'
    assert product.country == 'Франция'
    broken_product = Products('Парфюмерная вода THOMAS KOSMALA  № 5 Frénésie',
                              '3.8',
                              '20 313',
                              'https://goldapple.ru/28330100006-no-5-frenesie')
    broken_product.get_more_information_about_products()
    assert broken_product.instruction == '-'
    assert broken_product.country == '-'


def test_str(product):
    assert str(product) == ('Название: Парфюмерная вода J.U.S Joyau Unique & Sensoriel  Sensoriel Ambraser, \n'
                            'Рейтинг: 4.7, \n'
                            'Цена: 7 850, \n'
                            'URL: https://goldapple.ru/19000153561-sensoriel-ambraser, \n'
                            'Описание: None, \n'
                            'Инструкция: None, \n'
                            'Страна: None')
