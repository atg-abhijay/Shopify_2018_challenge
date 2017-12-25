import math
from pprint import pprint
import requests
from tinydb import TinyDB, Query

db = TinyDB('db.json')
menus = db.table('menus')
result_json = {'valid_menus': [], 'invalid_menus': []}
base_url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=2&page="

# sending requests and
# building the menus table
def build_menus():
    iterations = extract_iterations()
    # print(iterations)
    for page_num in range(1, iterations+1):
        url = base_url + str(page_num)
        r = requests.get(url)
        print(r.status_code)
        data = r.json()
        menus_value = data['menus']
        for menu_entry in menus_value:
            menu_entry['visited'] = False
            menus.insert(menu_entry)

    # print(menus.all())

def generate_result():
    # obtaining the top-level nodes
    # (menus without parent ids)
    menu_query = Query()
    top_nodes = menus.search(~ menu_query.parent_id.exists())
    for menu in top_nodes:
        # list of ids forming a path
        path = []
        updated_menu_id = menus.update({'visited': True}, menu_query.id == menu['id'])[0]
        # adding top level id to path
        path.append(updated_menu_id)
        isValid = check_children(menus.get(menu_query.id == updated_menu_id), path)
        if isValid:
            add_to_valid_menus(path)
        else:
            add_to_invalid_menus(path)

    menus.update({'visited': False})
    pprint(result_json)

def check_children(menu, path):
    valid_boolean = False
    menu_query = Query()
    for child_id in menu['child_ids']:
        # adding child id to list of ids
        path.append(child_id)
        child_menu = menus.search(menu_query.id == child_id)[0]
        if child_menu['visited']:
            valid_boolean = False
            # add_to_invalid_menus(path)
        elif len(child_menu['child_ids']) == 0:
            menus.update({'visited': True}, menu_query.id == child_id)
            valid_boolean = True
            # add_to_valid_menus(path)
        else:
            menus.update({'visited': True}, menu_query.id == child_id)
            check_children(menus.get(menu_query.id == child_id), path)

    return valid_boolean

def add_to_invalid_menus(ids_list):
    ids_list.sort()
    invalids = result_json['invalid_menus']
    root_id = ids_list[0]
    children = ids_list[1:]
    invalids.append({'root_id': root_id, 'children': children})


def add_to_valid_menus(ids_list):
    ids_list.sort()
    valids = result_json['valid_menus']
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
    # num_iterations = math.ceil(y/x)
    # print(num_iterations)

    # for i in range(1, 2):
    #     print(i)

    menu_query = Query()
    example_id = 2
    return_val = menus.update({'visited': True}, menu_query.id == example_id)[0]
    print(return_val)

    print(menus.get(menu_query.id == 2))

purge()
build_menus()
generate_result()
# test()
