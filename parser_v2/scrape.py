import json
from pathlib import Path

import requests as req
from bs4 import BeautifulSoup

from .config import HEADERS, TAG, PROP, DESC

path = Path(__file__)
path = path.parent.joinpath("data")
# Need for create 'data' dir
folder_path = "./parser_v2/data"


class Scrape:
    def __init__(self):
        self.fmt = ".json"

    def soup(self, url):
        response = req.get(url, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            soup = None
        return soup

    def write_data_to_file(self, data, fname):
        if not Path(folder_path).exists():
            Path(folder_path).mkdir()
            print(f"Folder '{folder_path}' was created.")
        else:
            print(f"Folder '{folder_path}' already exists.")

        with open(f"{path}/{fname}{self.fmt}", mode="w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"'{fname}{self.fmt}' OK")

    def get_urls(self, url, write=False):
        soup = self.soup(url).select(TAG[0])
        self.links = []
        for link in soup:
            link = link.get("href")
            if link not in self.links:
                if "product" not in link:
                    self.links.append(link)
        if write:
            self.write_data_to_file(self.links, "pages")
        return self.links

    def get_products_urls(self, write=False):
        if "shop" in self.links[0]:
            soup = self.soup(self.links[0]).select(TAG[1])
            self.items = []
            for item in soup:
                item = item.get("href")
                if item not in self.items:
                    self.items.append(item)
            if write:
                self.write_data_to_file(self.items, "item_pages")
            return self.items
        return None


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
        if soup.find("meta", property=PROP[0]):
            price = soup.find("meta", property=PROP[0]).get("content")
        elif soup.select_one(PROP[1]):
            self.price = soup.select_one(PROP[1]).text
        return f"{price}" + " \u20B4"  # '₴'

    def get_description(self):
        soup = self.soup
        desc = None
        if soup.find("meta", property=DESC[0]):
            desc = soup.find("meta", property=DESC[0]).get("content")
        elif soup.find("meta", property=DESC[1]):
            desc = soup.find("meta", property=DESC[1]).get("content")
        elif soup.find("meta", property=DESC[2]):
            desc = soup.find("meta", property=DESC[2]).get("content")
        elif soup.find("p"):
            desc = soup.find("p").contents
        return (
            desc.replace("\t\t\t", "\n")
            .replace("\t\t", "\n")
            .replace("\t", "\n")
        )

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
