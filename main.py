from config import *
from i_phone12 import *
import json
import re


def main():
    get_suche_page(url_sofort_kaufen, 2, headers=headers)
    print(products_list_ist)
    save_dict_to_json(products_list_ist,"products_list")
    print(read_from_json_to_dict("products_list"))
    





if __name__ == '__main__':
    main()
