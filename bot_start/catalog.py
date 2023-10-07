import json
from pathlib import Path
from parser_v2.config import fname_catalog

PATH = Path(__file__).parent.parent.joinpath("parser_v2/data")


def read_catalog():
    with open(f"{PATH}/{fname_catalog}") as json_file:
        catalog = json.load(json_file)
    return catalog


if __name__ == "__main__":
    read_catalog()

#   item_id = catalog['hair2']["product_id"]
#   qty = 2
#   order = f"{URL}checkout/?add-to-cart={item_id}&quantity={qty}"
