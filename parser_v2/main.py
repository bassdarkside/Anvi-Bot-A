from .scrape import Scrape, Item
from .config import fname_item_pages, fname_catalog


scrape = Scrape()


def scrape_url():
    scrape.urls(write=True)
    scrape.products_urls(write=True)


def make_catalog():
    catalog = {}
    links = scrape.read_data(fname_item_pages)
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
                "chapter": category,  # f"{category}{indx}",
                "name": meta.title(),
                "price": meta.price(),
                "image": meta.image(),
                "status": meta.status(),
                "product_id": meta.product_id(),
                "variations": meta.variations(),
                "description": meta.description(),
            }
            indx += 1
    # ./data/catalog.json
    scrape.write_data(catalog, fname_catalog)
    return catalog


if __name__ == "__main__":
    scrape_url()
    make_catalog()
