import json
import requests
from bs4 import BeautifulSoup
import re
import datetime
import csv

href_list = []
product_ids = []
products_list = {}
products_ids_ist = []
products_list_ist = {}
products_ids_verk = []
products_list_verk = {}


# загрузка супа
def get_suche_page(url: str, pages: int, headers):
    # получаем новый словарь с телефонами
    for page in range(1, pages + 1):
        r = requests.get(f'{url}{page}', headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        parser_product(soup)

    return soup


def parser_product(soup):
    global products_list_ist
    global products_ids_ist
    result = soup.find_all('div', {
        'class': 's-item__info clearfix'})
    for item in result:
        href = item.find('a', {'class': 's-item__link'})['href']
        id = re.findall(r'(?<=itm/)\d*', str(href))
        name = item.find('span', {'role': 'heading'}).text
        zustand = item.find('span', {'class': 'SECONDARY_INFO'}).text
        preis = item.find('span', {'class': 's-item__price'}).text
        datum_ls = re.findall(r'(?<="BOLD">)[\w\W]*?(?=\<\/span)', str(item.find('span', {'class': 'BOLD'})))
        # преобразование в датетайм.
        # try:
        #     datum_str = f'23 {datum_ls[0]}'
        #     datum = datetime.datetime.strptime(datum_str, '%y %d. %b. %H:%M')
        # except Exception as e:
        #     datum = None
        if id[0] != "123456":
            products_ids_ist.append(int(id[0]))
        # product = {int(id[0]): {'href': href}}
        products_list_ist[id[0]] = {"href": href,
                                         "zustand": zustand,
                                         "name": name,
                                         "preis": preis,
                                         "datum": datum_ls}

    del products_list_ist["123456"]
    # product_ids_ist.pop(0)








# чтение из файла в словарь

# Записываем ids в файл
def save_list_to_txt(list:list, file_name: str):
    with open(f'{file_name}.txt', 'w') as file:
        for item in list:
            file.write(str(item)+"\n")
    file.close()

# Считываем ids из файла в лист
def read_from_txt_to_list(file_name: str):
    result_dict = []
    with open(file_name, 'r') as file:
        content = file.readlines()
    for line in content:
        result_dict.append(int(line.strip()))
    file.close()
    return result_dict

# сопоставление двух списков и выдача разницы
def comparison_ids(list1, list2):
    result = []
    for id in list1:
        if id not in list2:
            result.append(id)
    return result

# запись словаря в файл json
def save_dict_to_json(dict, file_name):
    json_str = json.dumps(dict, default=serialize_datetime)
    with open(f"{file_name}.json", "w") as f:
        json.dump(json_str, f)
    f.close()

# чтение из json в переменную
def read_from_json_to_dict(file_name: str):
    with open(f"{file_name}.json", "r") as f:
        my_dict_from_file = json.load(f)
    return my_dict_from_file

# Определяем функцию для сериализации объектов datetime
def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()


def parser_data(product_ids: list, headers):
    global products_list_neu
    counter = 1
    for id in product_ids:
        print(f"Обрабатывают {counter}. продукт")
        r = requests.get(f'https://www.ebay.de/itm/{id}', headers=headers)
        try:
            soup = BeautifulSoup(r.text, 'lxml')
            # result = soup.find_all('div', {
            #     'class': 's-item__info clearfix'})
            # print(result)
            counter += 1
            product = soup.find('div', {'class': 'tabbable'}) \
                .find('div', {'class': 'ux-layout-section ux-layout-section--features'}) \
                .find_all('div', {'class': 'ux-layout-section__row'})

            for div in product:
                row_keys = div.find_all('div', {'class': 'ux-labels-values__labels-content'})
                row_value = div.find_all('div', {'class': 'ux-labels-values__values-content'})

                for i in range(0, len(row_keys)):
                    products_list_neu[id][row_keys[i].text] = row_value[i].text
        except Exception as e:
            print(f'Verkauft! ID: {id}')


# сравнение списков и вычисление времени объявления
def lists_vergleich(product_list: dict, product_ids_neu: list):
    global product_ids
    global verkauft_product_ids
    global products_list
    for i in product_ids_neu:
        temp = product_list.get(i)
        if temp is None:
           verkauft_product_ids.append(i)

