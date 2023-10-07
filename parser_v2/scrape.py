import json
from pathlib import Path
import requests as req
from bs4 import BeautifulSoup

from parser_v2.config import (
    fname_item_pages,
    fname_pages,
    HEADERS,
    CLASS,
    DESC,
    URL,
    TAG,
)

path = Path(__file__).parent.joinpath("data")


class Scrape:
    def soup(self, url):
        response = req.get(url, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            soup = None
        return soup

    def write_data(self, data, fname):
        if not Path(path).exists():
            Path(path).mkdir()
            print("Folder '/parser_v2/data' was created.")
        with open(f"{path}/{fname}", mode="w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"'{fname}' OK")

    def read_data(self, fname):
        with open(f"{path}/{fname}", mode="r") as f:
            data = json.load(f)
            return data

    def urls(self, write=False):
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
            self.write_data(self.links, fname_pages)
        return self.links

    def products_urls(self, write=False):
        categories_links = self.read_data(fname_pages)
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
            self.write_data(self.category_items, fname_item_pages)
        return self.category_items


class Item:
    def __init__(self, item_url):
        self.scrape = Scrape()
        self.soup = self.scrape.soup(item_url)

    def title(self):
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

    def price(self):
        soup = self.soup
        price = None
        if soup.select('p[class="price product-page-price"]'):
            price = soup.select('p[class="price product-page-price"]')
            for p in price:
                price = p.text
        if soup.select('vid[class="price-wrapper"]'):
            price = soup.select('vid[class="price-wrapper"]')
            for p in price:
                price = p.text
        elif soup.select('p[class="price product-page-price price-on-sale"]'):
            price = soup.select(
                'p[class="price product-page-price price-on-sale"]'
            )
            for p in price:
                price = p.text
        if len(price) > 6:
            return price[1:4:]

        return price[1:4:]  # + " \u20B4" # '₴'

    def description(self):
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

    def image(self):
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

    def status(self):
        soup = self.soup
        status = None
        if soup.select_one(CLASS[2]):
            status = soup.select_one(CLASS[2]).text
        return status

    def product_id(self):
        soup = self.soup
        item_id = None
        if soup.find("button", {"name": "add-to-cart"}):
            item_id = soup.find("button", {"name": "add-to-cart"}).get("value")
        if soup.select_one("div[data-product_id]"):
            item_id = soup.select_one("div[data-product_id]").get(
                "data-product_id"
            )
        return item_id

    def variations(self):
        soup = self.soup
        vid = []
        if soup.select_one("form[data-product_variations]"):
            variants = soup.select_one("form[data-product_variations]")
            vario = json.loads(variants.get("data-product_variations"))
            for n in range(len(vario)):
                if vario[n]["variation_is_active"]:
                    attr = (
                        vario[n]["variation_id"],
                        vario[n]["attributes"]["attribute_pa_vaha"],
                        vario[n]["attributes"]["attribute_pa_pakuvannia"],
                    )
                    vid.append(attr)
        return vid
