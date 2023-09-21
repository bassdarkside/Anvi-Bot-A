import json
import re
import requests
from bs4 import BeautifulSoup
from . import cfg


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
    res = re.sub(clean, "", text).replace("&nbsp;", "")
    return "".join(res)


def get_all_products_data(urls):
    cat_id = "1380b703-ce81-ff05-f115-39571d94dfcd"
    alldata = {}
    for i in range(len(urls)):
        soup = get_soup(urls[i])
        data = soup.find("script", id="wix-warmup-data")
        data = data.get_text(strip=True)
        product = json.loads(data)["appsWarmupData"][cat_id][cfg.KEYS[i]][
            "catalog"
        ]["product"]

        name = product["name"].capitalize()
        price = product["formattedPrice"]
        status = product["inventory"]["status"].replace("_", " ").capitalize()
        url = product["urlPart"]
        url_ = f"{cfg.URL}/product-page/{url}"
        description = cleaning_str(product["description"]).strip()
        item = {
            f"item{i+1}": {
                "name": name,
                "price": price,
                "status": status,
                "url": url_,
                "description": description,
            }
        }
        alldata.update(item)
    return alldata


def about(about_url):
    soup = get_soup(about_url)
    about = soup.select_one("#comp-ldbsxtoz").get_text()
    return about


def delivery(delivery_url):
    soup = get_soup(delivery_url)
    delivery = soup.select_one("div[id='comp-ldbsxypn3']").get_text()
    return delivery


def faq(faq_url):
    faq_tags = [
        "div[id='comp-ldbsxu9b4']",
        "div[id='comp-ldbsxu9b7']",
        "div[id='comp-ldbsxu9c']",
    ]
    soup = get_soup(faq_url)
    faq = ""
    for data in faq_tags:
        faq += f"\n{soup.select_one(data).get_text()}"
    return faq


def write_data_to_file(data, filename):
    path = "/Users/serhii/vs_code_projects/3_11_4/my_projector/bot_tg/parser_v2_1/data/"
    # path = "data/"
    with open(f"{path}{filename}", mode="w", newline="") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    print("Starting parser..")
    cat = get_all_products_data(cfg.PRODUCTS_PAGES)
    write_data_to_file(cat, filename="all_catalog.json")

    # about_ = about(cfg.ABOUT)
    # write_data_to_file(about_, filename="about.json")

    # delivery_ = delivery(cfg.DELIVERY)
    # write_data_to_file(delivery_, filename="delivery.json")

    # faq_ = faq(cfg.FAQ_PAGE)
    # write_data_to_file(faq_, filename="faq.json")
    return "Parser is finish!"


if __name__ == "__main__":
    main()
