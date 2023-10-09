from .scrape import Scrape, Item
from .config import ITEMS, CATALOG


scrape = Scrape()


def scrape_url():
    scrape.urls()
    scrape.products_urls()


def make_catalog():
    catalog = {}
    links = scrape.read_data(ITEMS)
    print("Collecting catalog..")
    for category in links.keys():
        indx = 1
        for link in links[category]:
            key = f"{category}{indx}"
            meta = Item(link)
            if "karta" in link:
                key = "gift_card"
                indx -= 1
            catalog[key] = {
                "url": link,
                "chapter": category,
                "name": meta.name(),
                "price": meta.price(),
                "price_int": meta.price_int(),
                "image": meta.image(),
                "status": meta.status(),
                "product_id": meta.product_id(),
                "variations": meta.variations(),
                "description": meta.description(),
            }
            indx += 1
    # ./data/catalog.json
    scrape.write_data(catalog, CATALOG)
    return catalog


def other_pages():
    faq = scrape.faq()
    about = scrape.about()
    return faq, about


if __name__ == "__main__":
    scrape_url()
    other_pages()
    make_catalog()
