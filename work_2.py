import json
import re
import time

import requests
from bs4 import BeautifulSoup

with open('product.json') as f:
    file = json.load(f)

final_result = []
counter = 0
for i in file:
    r = requests.get(i['url'])
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

    # опять же, сделал проверку, что бы при отсутствии инструкции не заходил не туда и не брал ненужную информацию
    if re.search('[a-zA-Z]', instruction):
        instruction = '-'

    country = instruction_country.findChildren(recursive=False)[-1]
    country = country.find('div').find('div').text

    # вот так решил получать страну
    try:
        country = country.split('страна происхождения', 1)[1]
        country = country.split('изготовитель', 1)[0]
    except:
        country = '-'

    i['description'] = description
    i['instruction'] = instruction
    i['country'] = country
    final_result.append(i)
    time.sleep(1)
    counter += 1
    print(counter)


with open('final_product_2.json', 'w') as f:
    json.dump(final_result, f, indent=4, ensure_ascii=False)
