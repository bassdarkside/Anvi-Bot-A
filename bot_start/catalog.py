import json
from pathlib import Path
from collections import OrderedDict

PATH = Path("Anvi-Bot-A/parser_v2/data")


def read_catalog_from_file():
    with open(f"{PATH}/catalog.json") as json_file:
        items_cat = json.load(json_file)
    items_ord = OrderedDict()
    items_cat["5"], items_cat["6"] = items_cat["6"], items_cat["5"]

    for i in range(5, 14):
        new_key = i - 4
        items_ord[str(new_key)] = items_cat[str(i)]

    items_ord[str(10)] = items_cat["1"]
    items_ord[str(11)] = items_cat["3"]
    items_ord[str(12)] = items_cat["4"]
    items_ord[str(13)] = items_cat["2"]

    for num in range(1, 4):
        items_ord[f"{num}"]["chapter"] += "1"
    for num in range(4, 7):
        items_ord[f"{num}"]["chapter"] += "2"
    for num in range(7, 10):
        items_ord[f"{num}"]["chapter"] += "3"
    for num in range(10, 13):
        items_ord[f"{num}"]["chapter"] += "4"
    items_ord["13"]["chapter"] += "5"

    return items_ord


if __name__ == "__main__":
    read_catalog_from_file()
