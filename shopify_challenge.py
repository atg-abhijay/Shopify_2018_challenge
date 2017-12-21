import requests
from tinydb import TinyDB, Query
import math

db = TinyDB('db.json')
menus = db.table('menus')
base_url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page="

def main():
    iterations = extract_iterations()
    # print(iterations)
    # TODO if iterations == 1, then
    # loop will not run
    for page_num in range(1, iterations+1):
        url = base_url + str(page_num)
        r = requests.get(url)
        print(r.status_code)
        data = r.json()
        menus_value = data['menus']
        for menu_entry in menus_value:
            menus.insert(menu_entry)

    print(menus.all())


def extract_iterations():
    url = base_url + str(1)
    r = requests.get(url)
    data = r.json()
    pagination_data = data['pagination']
    per_page = pagination_data['per_page']
    total_items = pagination_data['total']
    return math.ceil(total_items/per_page)

def purge():
    menus.purge()

def test():
    # x = 5
    # y = 15
    # result = math.ceil(y/x)
    # print(result)
    for i in range(1,3):
        print(i)


purge()
main()
# test()

