import json
from pathlib import Path
import requests as req
from bs4 import BeautifulSoup

from parser_v2.config import (
    DATAPATH,
    CONTACTS,
    HEADERS,
    ITEMS,
    ABOUT,
    PAGES,
    CLASS,
    DESC,
    URL,
    TAG,
)


class Scrape:
    def soup(self, url):
        response = req.get(url, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            soup = None
        return soup

    def write_data(self, data, fname):
        if not Path(DATAPATH).exists():
            Path(DATAPATH).mkdir()
            print("Folder '/parser_v2/data' was created.")
        with open(f"{DATAPATH}/{fname}", mode="w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"'{fname}' OK")

    def read_data(self, fname):
        with open(f"{DATAPATH}/{fname}", mode="r") as f:
            data = json.load(f)
            return data

    def urls(self, write=True):
        soup = self.soup(URL).select(TAG[0])
        category = []
        self.links = {}
        for link in soup:
            link = link.get("href")
            if "category" in link:
                category.append(link)
            if "kontakty" in link:
                contacts = link
            if "about" in link:
                about = link
        self.links = {
            "about": about,
            "contacts": contacts,
            "categories": category,
        }
        if write:
            self.write_data(self.links, PAGES)
        return self.links

    def products_urls(self, write=True):
        categories_links = self.read_data(PAGES)
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
            self.write_data(self.category_items, ITEMS)
        return self.category_items

    def contacts(self):
        contacts = ""
        head = self.soup(self.links["contacts"]).select("h3")
        body = self.soup(self.links["contacts"]).select("h3 ~ p")
        for i in range(len(body)):
            contacts += head[i].getText() + "\n" + body[i].getText() + "\n\n"
        self.write_data(contacts, CONTACTS)
        return contacts

    def about(self):
        soup = self.soup(self.links["about"])
        header = soup.select("h2[class='MW5IWV']")
        soup = soup.select("p[class='MW5IWV']")
        about = header[0].getText() + "\n\n"
        for text in soup[:8]:
            about += text.getText()
        about += "\n\n"
        for text2 in soup[8:12]:
            about += text2.getText()
        about += "\n\n" + header[1].getText() + "\n\n"
        for text2 in soup[12:]:
            about += text2.getText()
        self.write_data(about, ABOUT)
        return about


class Item:
    def __init__(self, item_url):
        self.scrape = Scrape()
        self.soup = self.scrape.soup(item_url)

    def name(self):
        soup = self.soup
        name = None
        try:
            name = soup.select('script[type="application/ld+json"]')
            name = json.loads(name[1].getText())
            return name["@graph"][1]["name"]
        except KeyError:
            pass

    def price(self):
        soup = self.soup
        price = None
        if soup.select('p[class="price product-page-price"]'):
            price = soup.select('p[class="price product-page-price"]')
            for p in price:
                price = p.text.strip()
            return price
        try:
            price = soup.select('script[type="application/ld+json"]')
            price = json.loads(price[1].getText())
            low_price = price["@graph"][1]["offers"][0]["lowPrice"]
            hi_price = price["@graph"][1]["offers"][0]["highPrice"]
            price = f"{low_price} ₴ – {hi_price} ₴"
            return price
        except Exception:
            pass

    def price_int(self):
        soup = self.soup
        price_int = None
        try:
            price_int = soup.select('script[type="application/ld+json"]')
            price_int = json.loads(price_int[1].getText())
            price_int = price_int["@graph"][1]["offers"][0]["price"]
            return int(price_int)
        except KeyError:
            pass

    def description_short(self):
        soup = self.soup
        description = None
        try:
            description = soup.select('script[type="application/ld+json"]')
            description = json.loads(description[1].getText())
            return description["@graph"][1]["description"].strip()
        except Exception:
            pass

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
        try:
            img = soup.select('script[type="application/ld+json"]')
            img = json.loads(img[1].getText())
            return img["@graph"][1]["image"]
        except Exception:
            pass

    def status(self):
        soup = self.soup
        status = None
        if soup.select_one(CLASS[2]):
            status = soup.select_one(CLASS[2]).text
        return status

    def product_id(self):
        soup = self.soup
        item_id = None
        try:
            item_id = soup.select('script[type="application/ld+json"]')
            item_id = json.loads(item_id[1].getText())
            item_id = item_id["@graph"][1]["sku"]
            return str(item_id)
        except Exception:
            pass

    def variations(self):
        soup = self.soup
        options = {}
        if soup.select_one("form[data-product_variations]"):
            variants = soup.select_one("form[data-product_variations]")
            variants = json.loads(variants.get("data-product_variations"))
            for n in range(len(variants)):
                name = ""
                vario = variants[n]
                price = vario["display_price"]
                if vario["variation_is_active"]:
                    id = vario["variation_id"]
                    weight = vario["attributes"]["attribute_pa_vaha"]
                    packing = vario["attributes"]["attribute_pa_pakuvannia"]
                    if packing == "aliuminiieva-upakovka":
                        name = "алюмінієва упаковка"
                        packing = "a"
                    if packing == "paperova-upakovka":
                        name = "паперова упаковка"
                        packing = "p"
                    if packing == "sklana-pliashka-z-aliuminiievoiu-kryshkoiu":
                        name = "скляна пляшка з алюмінієвою кришкою"
                        packing = "alum"
                    if packing == "sklana-pliashka-z-krapelnychkoiu":
                        name = "скляна пляшка з крапельничкою"
                        packing = "drop"
                    opt = {
                        f"{packing}{weight[:2:]}": {
                            "vario_id": str(id),
                            "vario_price": price,
                            "vario_weight": weight[:2:],
                            "packing_name": name,
                        }
                    }
                    options.update(opt)
        return options
