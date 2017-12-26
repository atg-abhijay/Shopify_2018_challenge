from math import ceil
from pprint import pprint
import sys, requests
from tinydb import TinyDB, Query

db = TinyDB('db.json')
menus = db.table('menus')
result_json = {'valid_menus': [], 'invalid_menus': []}

# url of the challenge without the page number value
# url decided from run() method
base_url = ""


def build_menus():
    """
    sending requests and
    building the menus table
    """
    # call the extract_iterations() method
    # to identify the number of pages to
    # be visited
    iterations = extract_iterations()
    for page_num in range(1, iterations+1):
        # append page number to base_url
        # to get a specific page
        url = base_url + str(page_num)
        print("Building menus...")
        r = requests.get(url)
        print(r.status_code)
        data = r.json()
        menus_value = data['menus']
        for menu_entry in menus_value:
            # adding another field 'visited'
            # to each of the nodes, so as to
            # manage their visit status
            menu_entry['visited'] = False
            menus.insert(menu_entry)

    # the menus table is now complete
    # (with the additional 'visited' field)


def generate_result():
    """
    method where all the 'calculations' are
    performed to identify valid and invalid menus
    """
    # obtaining the top-level nodes
    # (menus without parent ids).
    # these nodes will serve as root nodes

    # creating a query object for the db
    menu_query = Query()
    # searching for entities in the
    # menus table which do NOT have a
    # parent_id field. (the tilda '~'
    # is for negating the query)
    top_nodes = menus.search(~ menu_query.parent_id.exists())
    print("Generating results...")
    for menu in top_nodes:
        # list of ids forming a path
        path = []
        # update the database and set the 'visited'
        # status of the top_node to True
        updated_menu_id = menus.update({'visited': True}, menu_query.id == menu['id'])[0]
        # adding the id of top_node to path
        path.append(updated_menu_id)
        # calling check_children() with the current
        # top_node and the path. it traverses through
        # all the children rooted at the top_node and
        # returns a boolean value telling us whether
        # the menu is valid or invalid
        print("Checking children...")
        isValid = check_children(menus.get(menu_query.id == updated_menu_id), path)
        if isValid:
            # add path to valid_menus
            add_to_valid_menus(path)
        else:
            # add path to invalid_menus
            add_to_invalid_menus(path)

    # reset the field 'visited' to
    # False for all the nodes
    menus.update({'visited': False})

    # printing the final result
    pprint(result_json)


def check_children(menu, path):
    """
    traverses through the children of
    any menu and appends the ids of the
    visited menus to the path

    in the end it returns a boolean value
    indicating whether the path denotes a
    valid menu or an invalid menu
    """
    valid_boolean = False
    menu_query = Query()
    for child_id in menu['child_ids']:
        # adding id of child menu to list of ids
        path.append(child_id)
        # obtaining child menu from database
        child_menu = menus.search(menu_query.id == child_id)[0]
        # if the child menu has already been
        # visited then this indicates a cycle
        # and therefore we have an invalid menu
        if child_menu['visited']:
            valid_boolean = False

        # if the child menu has no children of its
        # own then we have reached the end along one
        # specific branch and it is valid (we set its
        # 'visited' status to True)
        #
        # if we get valid for all branches, then we
        # have a valid menu
        elif len(child_menu['child_ids']) == 0:
            menus.update({'visited': True}, menu_query.id == child_id)
            valid_boolean = True

        # if the child menu has children of its
        # own, then we recursively call check_children()
        # on its children (we set the current child's
        # 'visited' status to True)
        else:
            menus.update({'visited': True}, menu_query.id == child_id)
            check_children(menus.get(menu_query.id == child_id), path)

    # returning a boolean indicating whether
    # the menu is valid or invalid
    return valid_boolean


def add_to_invalid_menus(ids_list):
    """
    list of ids that constitute
    an invalid menu. the first id
    in the list is the root id
    and the rest are the children id
    """
    invalids = result_json['invalid_menus']
    root_id = ids_list[0]
    children = ids_list[1:]
    invalids.append({'root_id': root_id, 'children': children})


def add_to_valid_menus(ids_list):
    """
    list of ids that constitute
    a valid menu. the first id
    in the list is the root id
    and the rest are the children id
    """
    valids = result_json['valid_menus']
    root_id = ids_list[0]
    children = ids_list[1:]
    valids.append({'root_id': root_id, 'children': children})


def extract_iterations():
    """
    using the information from
    'pagination' to calculate the number
    of pages to visit (iterations)
    to get all the data
    """
    url = base_url + str(1)
    r = requests.get(url)
    data = r.json()
    pagination_data = data['pagination']
    per_page = pagination_data['per_page']
    total_items = pagination_data['total']
    return ceil(total_items/per_page)


def purge():
    """
    emptying the menus table
    """
    menus.purge()


def test():
    """
    test method to experiment
    different commands and
    strategies
    """
    x = 5
    y = 15
    num_iterations = ceil(y/x)
    print(num_iterations)

    for i in range(1, 2):
        print(i)

    menu_query = Query()
    example_id = 2
    return_val = menus.update({'visited': True}, menu_query.id == example_id)[0]
    print(return_val)

    print(menus.get(menu_query.id == 2))
    print(sys.argv[1])


def run():
    """
    First method that gets called.
    Depending on which command line
    argument is passed (either 1 or 2),
    output for challenge 1 or challenge 2
    (extra challenge) is produced
    """
    global base_url
    challenge_number = sys.argv[1]
    if challenge_number == "1":
        base_url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page="

    elif challenge_number == "2":
        base_url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=2&page="

    else:
        print("Please enter either 1 or 2")
        sys.exit(1)

run()
purge()
build_menus()
generate_result()
# test()
