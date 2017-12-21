import requests
from tinydb import TinyDB, Query
import math

db = TinyDB('db.json')
menus = db.table('menus')
base_url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page="

def main():
    data_list = [4,5]
    page_number = 1
    while not data_list:
        url = base_url + str(page_number)
        r = requests.get(url)
        data = r.json()
        data_list = data['menus']
    print(data_list)
    for menu_entry in data_list:
        menus.insert(menu_entry)

    # print(menus.all())
    print(r.status_code)

def extract_iterations():
    url = base_url + str(1)
    r = requests.get(url)
    data = r.json()
    pagination_data = data['pagination']
    per_page = pagination_data['per_page']
    total_items = pagination_data['total']
    print(per_page)
    print(total_items)

def purge():
    menus.purge()

def test():
    x = 5
    y = 15
    result = math.ceil(y/x)
    print(result)

extract_iterations()
# test()
# main()
# purge()
