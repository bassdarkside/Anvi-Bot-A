import json
from pathlib import Path
from parser_v2.config import CATALOG

PATH = Path(__file__).parent.parent.joinpath("parser_v2/data")

catalog = {
    "body": {
        "markup": "body",
        "chapter_name": "Тіло",
        "message": "Фізіологічні дезодоранти, крем для рук",
        "items": ["body1", "body3", "body4"],  # "body2"
        "chapter_img": "https://anvibodycare.com/wp-content/uploads/2023/09/katehoriia-1-300x300.jpg",
    },
    "face": {
        "markup": "face",
        "chapter_name": "Бальзами для губ",
        "message": "Бальзами для губ і не тільки",
        "items": ["face1", "face2", "face3"],
        "chapter_img": "https://anvibodycare.com/wp-content/uploads/2023/09/katehoriia-2-300x300.jpg",
    },
    "hair": {
        "markup": "hair",
        "chapter_name": "Волосся",
        "message": "Шампуні та бальзами",
        "items": ["hair1", "hair2", "hair3", "hair4", "hair5", "hair6"],
        "chapter_img": "https://anvibodycare.com/wp-content/uploads/2023/09/katehoriia-3-300x300.jpg",
    },
    "gift_card": {
        "markup": "gift_card",
        "chapter_name": "Подарункова карта",
        "message": "ANVI — український бренд.\n Поєднуючи веганську косметику та кращі активні інградієнти, ми підклуємося про вас.\n Використовуючи натуральні тари ми піклуємося про довкілля.",
        "items": ["gift_card"],
        "chapter_img": "https://anvibodycare.com/wp-content/uploads/2023/09/podarunkovyj-sertyfikat.jpg",
    },
}


def read_catalog():
    with open(f"{PATH}/{CATALOG}") as json_file:
        data = json.load(json_file)
    return data


if __name__ == "__main__":
    read_catalog()
