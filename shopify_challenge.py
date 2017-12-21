import math
import requests
from tinydb import TinyDB, Query
from pprint import pprint

db = TinyDB('db.json')
menus = db.table('menus')
result = {'valid_menus': [], 'invalid_menus': []}
base_url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page="

def build_menus():
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
            menu_entry['visited'] = False
            menus.insert(menu_entry)

    print(menus.all())

def generate_result():
    all_menus = menus.all()
    # obtaining the top-level nodes
    menu_query = Query()
    top_nodes = menus.search(~ menu_query.parent_id.exists())
    all_paths = []
    for menu in top_nodes:
        path = []
        if menu['visited'] == "false":
            menu['visited'] = "true"
            # adding top level id to path
            path.append(menu['id'])
            for child_id in menu['child_ids']:
                path.append(child_id)
                child_menu = menus.get(doc_id=child_id)
                if child_menu['visited'] == "true"



    # queue.append(all_menus[0])
    # print(queue)

def add_to_invalid_menus(ids_list):
    invalids = result['invalid_menus']
    root_id = ids_list[0]
    children = ids_list[1:]
    invalids.append({'root_id': root_id, 'children': children})


def add_to_valid_menus(ids_list):
    valids = result['valid_menus']
    root_id = ids_list[0]
    children = ids_list[1:]
    valids.append({'root_id': root_id, 'children': children})


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

    # for i in range(1,3):
    #     print(i)


    result = menus.search(~ menu_query.parent_id.exists())
    pprint(result)


# purge()
# build_menus()
# generate_result()
test()

