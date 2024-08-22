import json

from bs4 import BeautifulSoup
from selenium import webdriver

import time

url_gold_apple = 'https://goldapple.ru/parfjumerija'


def scrolldown(drive, deep):
    """Функция для скрола страницы"""
    for _ in range(deep):
        drive.execute_script('window.scrollBy(0, 500)')
        time.sleep(0.5)


def get_mainpage_cards(drive, url):
    """Функция для получения со страницы названия, рейтинга, цены и url продукта"""
    drive.get(url)
    scrolldown(drive, 50)
    main_page_html = BeautifulSoup(drive.page_source, 'lxml')

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
                except:
                    continue
                con = i.find('a')
                con = con.findChildren(recursive=False)[-1]

                price = con.findChildren(recursive=False)[-1]
                price = price.find('div').text.split('₽', 1)[0].strip()

                name = con.findChildren(recursive=False)[-2]
                name = name.find('div').text.strip()
                # Сделал такую проверку что бы не заходило не туда
                if 'Пятница' and '%' in name:
                    name = con.findChildren(recursive=False)[-3]
                    name = name.find('div').text.strip()

                    type_product = con.findChildren(recursive=False)[-4].text.strip()
                    # Не у всех товаров есть рейтинг, поэтому заходит не туда и падает с ошибкой
                    try:
                        stars = con.findChildren(recursive=False)[-5]
                        stars = stars.find('div').find('div').text.strip()
                    except:
                        stars = '-'

                else:
                    type_product = con.findChildren(recursive=False)[-3].text.strip()

                    try:
                        stars = con.findChildren(recursive=False)[-4]
                        stars = stars.find('div').find('div').text.strip()
                    except:
                        stars = '-'
                if '.' not in stars:
                    stars = '-'
                if 'от' in price:
                    price = price[6:]
                # article = url[1:12]
                full_name = type_product + ' ' + name
                result = {
                    'name': full_name,
                    'rating': stars,
                    'price': price,
                    'url': 'https://goldapple.ru' + url,
                }
                all_parfumes.append(result)

        except:
            continue
    return all_parfumes


# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver = webdriver.Chrome()
p = get_mainpage_cards(driver, url_gold_apple)
driver.quit()
# записал в json что бы постоянно не запускать код и дальше работать уже с джейсоном
with open('product.json', 'w') as f:
    json.dump(p, f, indent=4, ensure_ascii=False)
