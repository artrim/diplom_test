import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from src.scrolldown import scrolldown


class Products:
    url_gold_apple = 'https://goldapple.ru/parfjumerija'
    driver = webdriver.Chrome()

    def __init__(self, name, rating, price, url, description=None, instruction=None, country=None):
        self.name = name
        self.rating = rating
        self.price = price
        self.url = url
        self.description = description
        self.instruction = instruction
        self.country = country

    @classmethod
    def cast_to_object_list(cls):
        cls.driver.get(cls.url_gold_apple)
        scrolldown(cls.driver, 50)
        main_page_html = BeautifulSoup(cls.driver.page_source, 'lxml')
        # driver.get(url)
        # scrolldown(driver, 50)
        # main_page_html = BeautifulSoup(driver.page_source, 'lxml')

        content = main_page_html.find('main')
        content = content.findChildren(recursive=False)[-2]

        all_parfumes = []
        for layer in content:
            try:
                cards = layer.find('div')
                cards = cards.findChildren(recursive=False)

                for i in cards:
                    try:
                        url = i.find('a').get('href')
                    except Exception as e:
                        print(f'Произошла ошибка: {e}')
                        continue
                    con = i.find('a')
                    con = con.findChildren(recursive=False)[-1]

                    price = con.findChildren(recursive=False)[-1]
                    price = price.find('div').text.split('₽', 1)[0].strip()

                    name = con.findChildren(recursive=False)[-2]
                    name = name.find('div').text.strip()

                    if 'Пятница' and '%' in name:
                        name = con.findChildren(recursive=False)[-3]
                        name = name.find('div').text.strip()

                        type_product = con.findChildren(recursive=False)[-4].text.strip()
                        try:
                            rating = con.findChildren(recursive=False)[-5]
                            rating = rating.find('div').find('div').text.strip()
                        except Exception as e:
                            print(f'Произошла ошибка: {e}')
                            rating = '-'

                    else:
                        type_product = con.findChildren(recursive=False)[-3].text.strip()

                        try:
                            rating = con.findChildren(recursive=False)[-4]
                            rating = rating.find('div').find('div').text.strip()
                        except Exception as e:
                            print(f'Произошла ошибка: {e}')
                            rating = '-'

                    if '.' not in rating:
                        rating = '-'
                    if 'от' in price:
                        price = price[6:]

                    url = 'https://goldapple.ru' + url
                    full_name = type_product + ' ' + name
                    instance = cls(full_name, rating, price, url)
                    all_parfumes.append(instance)
            except Exception as e:
                print(f'Произошла ошибка: {e}')
                continue
            finally:
                # driver.quit()
                cls.driver.quit()
        return all_parfumes

    def get_other_information_about_products(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'lxml')
        content = soup.find('main').find('article')
        content = content.findChildren(recursive=False)[-1]
        content = content.findChildren(recursive=False)[-1]
        content = content.find('div')
        content = content.findChildren(recursive=False)[-1]

        product = content.find('div').find('div').find('div').find('div')
        description = product.findChildren(recursive=False)[-2].text

        instruction_country = content.find('div').find('div')
        instruction = instruction_country.findChildren(recursive=False)[1]
        instruction = instruction.find('div').find('div').text.strip()

        if re.search('[a-zA-Z]', instruction):
            instruction = '-'

        country = instruction_country.findChildren(recursive=False)[-1]
        country = country.find('div').find('div').text

        try:
            country = country.split('страна происхождения', 1)[1]
            country = country.split('изготовитель', 1)[0]
        except Exception as e:
            print(f'Произошла ошибка: {e}')
            country = '-'

        self.description = description
        self.instruction = instruction
        self.country = country

    def __str__(self):
        return (f'Название: {self.name}, \nРейтинг: {self.rating}, \nЦена: {self.price}, \nURL: {self.url}, '
                f'\nОписание: {self.description}, \nИнструкция: {self.instruction}, \nСтрана: {self.country}')
