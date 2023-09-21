import json

PATH = "bot_tg/parser_v2_1/data/"


def get_data_from_file():
    with open(f"{PATH}all_catalog.json") as json_file:
        items = json.load(json_file)

    catalog = {
        "chapter1": {
            "markup": "deodorants",
            "chapter_name": "Дезодорант (3)",
            "message": "Фізіологічні дезодоранти",
            "items": {
                "item1": items["item1"],
                "item2": items["item2"],
                "item3": items["item3"],
            },
        },
        "chapter2": {
            "markup": "balms",
            "chapter_name": "Бальзам для губ (3)",
            "message": "Бальзами для губ і не тільки",
            "items": {
                "item1": items["item4"],
                "item2": items["item5"],
                "item3": items["item6"],
            },
        },
        "chapter3": {
            "markup": "shampoo",
            "chapter_name": "Очищення (3)",
            "message": "Тверді шампуні",
            "items": {
                "item1": items["item7"],
                "item2": items["item8"],
                "item3": items["item9"],
            },
        },
        "chapter4": {
            "markup": "care",
            "chapter_name": "Догляд (3)",
            "message": "Бальзами для волосся",
            "items": {
                "item1": items["item10"],
                "item2": items["item11"],
                "item3": items["item12"],
                # "item4": items["item13"], # ?
            },
        },
    }
    return catalog


if __name__ == "__main__":
    get_data_from_file()
