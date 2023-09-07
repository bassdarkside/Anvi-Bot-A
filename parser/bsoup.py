import requests
from bs4 import BeautifulSoup
import json


def get_soup(url, **kwargs):
    response = requests.get(url, **kwargs)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features="html.parser")
    else:
        soup = None
    return soup


def parse_catalog(urls):
    catalog_data = {}
    for i, url in enumerate(urls, start=1):
        soup = get_soup(url)
        if soup is None:
            break
        name = soup.select_one("h1[data-hook]").text.strip().title()
        price = soup.select_one(
            "span[data-hook='formatted-primary-price']"
        ).text.strip()
        for ln in soup.select("pre[data-hook='description']"):
            ln = ln.select("p")
            description = [i.text.replace("\xa0", "") for i in ln]
        description = " ".join(i for i in description if i)
        item = {
            "name": name,
            "price": price,
            "url": url,
            "description": description,
        }
        catalog_data[i] = item
    return catalog_data


def about(about_url):
    soup = get_soup(about_url)
    for i in soup.select("#comp-ldbsxtoz"):
        about = [j.text.replace("\xa0", "") for j in i.select("p")]
    return "".join(i for i in about if i)


def delivery(delivery_url):
    soup = get_soup(delivery_url)
    for d in soup.select("div[id='comp-ldbsxypn3']"):
        delivery = [j.text.replace("\xa0", "") for j in d.select("p")]
    return "".join(i for i in delivery if i)


def main(URL, ABOUT, DELIVERY):
    soup = get_soup(URL)
    tag_a = soup.find_all("a", class_="JPDEZd")
    url = [link.get("href") for link in tag_a]
    data = {
        "catalog": parse_catalog(url),
        "delivery": delivery(DELIVERY),
        "about": about(ABOUT),
    }
    with open("parser/data/data.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


DELIVERY = "https://www.anvibodycare.com/політика-магазину"
ABOUT = "https://www.anvibodycare.com/%D0%BF%D1%80%D0%BE-%D0%BD%D0%B0%D1%81"
SHOP_URL = "https://www.anvibodycare.com/shop"

main(SHOP_URL, ABOUT, DELIVERY)
