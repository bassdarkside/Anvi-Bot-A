import json
from pathlib import Path

import requests as req
from bs4 import BeautifulSoup

from .config import (
    fname_item_pages,
    fname_pages,
    PROXIES,
    HEADERS,
    CLASS,
    DESC,
    PROP,
    URL,
    TAG,
)

path = Path(__file__).parent.joinpath("data")


class Scrape:
    def __init__(self):
        self.fmt = ".json"

    def soup(self, url):
        response = req.get(url, headers=HEADERS, proxies=PROXIES)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            soup = None
        return soup

    def write_data_to_file(self, data, fname):
        if not Path(path).exists():
            Path(path).mkdir()
            print("Folder '/parser_v2/data' was created.")
        with open(f"{path}/{fname}", mode="w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"'{fname}' OK")

    def read_data_from_file(self, fname):
        with open(f"{path}/{fname}", mode="r") as f:
            data = json.load(f)
            return data

    def get_urls(self, write=False):
        soup = self.soup(URL).select(TAG[0])
        category = []
        self.links = {}
        for link in soup:
            link = link.get("href")
            if "category" in link:
                category.append(link)
            if "faq" in link:
                faq = link
            if "about" in link:
                about = link
        self.links = {
            "faq": faq,
            "about": about,
            "categories": category,
        }
        if write:
            self.write_data_to_file(self.links, fname_pages)
        return self.links

    def get_products_urls(self, write=False):
        categories_links = self.read_data_from_file(fname_pages)
        body, face, hair = [], [], []
        self.category_items = {}
        for link in categories_links["categories"]:
            soup = self.soup(link).select(TAG[1])
            for item in soup:
                item = item.get("href")
                if item != "https://anvibodycare.com/shop/":
                    if "tilo" in link:
                        if item not in body:
                            body.append(item)
                    if "oblychchia" in link:
                        if item not in face:
                            face.append(item)
                    if "volossia" in link:
                        if item not in hair:
                            hair.append(item)
            self.category_items = {
                "body": body,
                "face": face,
                "hair": hair,
            }
        if write:
            self.write_data_to_file(self.category_items, fname_item_pages)
        return self.category_items


class Item:
    def __init__(self, item_url):
        self.scrape = Scrape()
        self.soup = self.scrape.soup(item_url)

    def get_title(self):
        soup = self.soup
        title = None
        if soup.title.string:
            title = soup.title.string
        elif soup.find("meta", property="og:title"):
            title = soup.find("meta", property="og:title").get("content")
        elif soup.find("meta", property="twitter:title"):
            title = soup.find("meta", property="twitter:title").get("content")
        elif soup.find("h1"):
            title = soup.find("h1").string
        elif soup.find_all("h1"):
            title = soup.find_all("h1")[0].string
        if title:
            title = title.split("|")[0]
        return title.capitalize()

    def get_price(self):
        soup = self.soup
        price = None
        if soup.find("p", class_=CLASS[0]):
            price = soup.find("p", class_=CLASS[0]).text
        if soup.find("meta", property=PROP[0]):
            price = soup.find("meta", property=PROP[0]).get("content")
        elif soup.select_one(PROP[1]):
            self.price = soup.select_one(PROP[1]).text
        return f"{price}"  # + " \u20B4" # '₴'

    def get_description(self):
        soup = self.soup
        desc = ""
        data = None
        if soup.select(CLASS[1]):
            data = soup.select(CLASS[1])
        elif soup.find("meta", property=DESC[1]):
            data = soup.find("meta", property=DESC[1]).text
        elif soup.find("meta", property=DESC[2]):
            data = soup.find("meta", property=DESC[2]).text
        elif soup.find("p"):
            data = soup.find("p").text
        for descript in data:
            desc += " " + descript.text
        return desc

    def get_image(self):
        soup = self.soup
        img = None
        if soup.find("meta", property="image"):
            img = soup.find("meta", property="image").get("content")
        elif soup.find("meta", property="og:image"):
            img = soup.find("meta", property="og:image").get("content")
        elif soup.find("meta", property="twitter:image"):
            img = soup.find("meta", property="twitter:image").get("content")
        elif soup.find_all("img", src=True):
            img = soup.find_all("img")
            if img:
                img = soup.find_all("img")[0].get("src")
        return img

    def get_status(self):
        soup = self.soup
        status = None
        if soup.select_one(CLASS[2]):
            status = soup.select_one(CLASS[2]).text
        return status
