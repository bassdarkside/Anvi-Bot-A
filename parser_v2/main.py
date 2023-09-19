import json
import re
import requests
from bs4 import BeautifulSoup
from config import (
    PRODUCTS_PAGES,
    KEYS,
    ABOUT,
    DELIVERY,
    FAQ_PAGE,
)


def get_soup(url):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
    else:
        soup = None
    return soup


def cleaning_str(text):
    clean = re.compile("<.*?>")
    res = (
        re.sub(clean, " ", text)
        .replace("&nbsp;", "")
        .replace("\t", "")
        .replace("\n", "")
        .split()
    )
    return " ".join(res)


def get_all_products_data(urls):
    alldata = []
    for i in range(len(urls)):
        soup = get_soup(urls[i])
        data = soup.find("script", id="wix-warmup-data")
        data = data.get_text(strip=True)

        product = json.loads(data)["appsWarmupData"][
            "1380b703-ce81-ff05-f115-39571d94dfcd"
        ][KEYS[i]]["catalog"]["product"]

        name = product["name"].capitalize()
        price = product["price"]  # -> int
        formatted_price = product["formattedPrice"]  # -> string
        is_in_stock = product["isInStock"]  # -> boolean
        status = (
            product["inventory"]["status"].replace("_", " ").capitalize()
        )  # -> string
        description = cleaning_str(product["description"])
        images = [
            product["media"][i]["fullUrl"]
            for i in range(len(product["media"]))
        ]
        additional_info = [
            f'{info["title"].capitalize()}: {cleaning_str(info["description"])}'
            for info in product["additionalInfo"]
        ]
        vol_weight = None
        if product["options"]:
            opt = product["options"][0]["selections"]
            vol_weight = [opt[i]["value"] for i in range(len(opt))]

        item = {
            "product_name": name,
            "price": price,
            "formatted_price": formatted_price,
            "is_in_stock": is_in_stock,
            "status": status,
            "description": description,
            "images": images,
            "additional_info": additional_info,
            "vol_weight": vol_weight,
        }
        alldata.append(item)
        write_data_to_file(
            item, filename="all_products_catalog.json", mode="a"
        )
    return alldata


def about(about_url):
    soup = get_soup(about_url)
    about = soup.select_one("#comp-ldbsxtoz").get_text()
    write_data_to_file(about.strip(), filename="about.json", mode="w")
    return about.strip()


def delivery(delivery_url):
    soup = get_soup(delivery_url)
    delivery = soup.select_one("div[id='comp-ldbsxypn3']").get_text()
    write_data_to_file(delivery.strip(), filename="delivery.json", mode="w")
    return delivery.strip()


def faq(faq_url):
    faq_tags = [
        "div[id='comp-ldbsxu9b4']",
        "div[id='comp-ldbsxu9b7']",
        "div[id='comp-ldbsxu9c']",
    ]
    soup = get_soup(faq_url)
    faq = ""
    for data in faq_tags:
        faq += f"{soup.select_one(data).get_text()}\n"
    write_data_to_file(faq.strip(), filename="faq.json", mode="w")
    return faq.strip()


def write_data_to_file(data, filename, mode):
    path = "data/"
    with open(f"{path}{filename}", mode) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    get_all_products_data(PRODUCTS_PAGES)
    about(ABOUT)
    delivery(DELIVERY)
    faq(FAQ_PAGE)
