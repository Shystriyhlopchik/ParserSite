from bs4 import BeautifulSoup
import requests
import json
import re


page = BeautifulSoup(requests.get('https://www.dme.ru/shopping/shop/').text, 'lxml')

shops = {}

element_selectors = [
    {
        'tag': 'div',
        'kwargs': {'class_': 'shadows_left'}
    },
    {
        'tag': 'div',
        'kwargs': {'class_': 'shadows_right'}
    },
    {
        'tag': 'div',
        'kwargs': {'class_': 'layout'}
    },
    {
        'tag': 'div',
        'kwargs': {'class_': 'main'}
    },
    {
        'tag': 'div',
        'kwargs': {'class_': 'right_column'}
    },
    {
        'tag': 'div',
        'kwargs': {'class_': 'content'}
    },
    {
        'tag': 'div',
        'kwargs': {'class_': 'simple'}
    },
    {
        'tag': 'div',
        'kwargs': {'class_': 'simple'}
    },
    {
        'tag': 'div',
        'kwargs': {}
    },
    {
        'tag': 'div',
        'kwargs': {}
    }
]
response = page

for selector in element_selectors:
    response = response.find(selector['tag'], **selector['kwargs'])

response = response.findAll(['a', 'h2', 'p'])

key_string = ''
for element in response:
    if element.name == 'h2':
        shops.update({element.text: {'name': element.text, 'location': 'Unknown', 'shops': []}})
        key_string = element.text

    elif key_string and element.name == 'p' and 'располож' in element.text:
        pattern = re.compile(r'расположен[а|ы]?([\w|\s]+)')
        shops[key_string]['location'] = re.split(pattern, element.text)[1].strip()

    elif key_string and element.name == 'a' and element.text:
        connect_string = "".join(
            re.findall(
                '(https?://)?(www\.)?([-\w.]+)',
                'https://www.dme.ru/shopping/shop/'
            )[0]
        )
        shop_url = connect_string + (
            element.attrs["href"] if element.attrs['href'][0] == '/' else f'/{element.attrs["href"]}')
        shops[key_string]['shops'].append({'name': element.text, 'url': shop_url})


with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(shops, f, indent=2, ensure_ascii=False)
