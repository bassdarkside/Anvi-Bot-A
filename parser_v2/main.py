import time
import random
from .scrape import Scrape, Item
from .config import fname_item_pages, fname_catalog


def run_scrape():
    """
    The `run` function scrapes product information from a website,
    stores it in a dictionary, and writes it to a JSON file.

    :return: The function `run()` is returning a dictionary `items_cat`
    which contains information aboutthe scraped items.

    Path file 'parser_v2/data/catalog.json'
    """
    scrape = Scrape()
    scrape.get_urls(write=True)
    scrape.get_products_urls(write=True)
    items_cat = {}
    item_urls = scrape.read_data_from_file(fname_item_pages)
    for cat in item_urls.keys():
        for indx, link in enumerate(item_urls[cat], start=1):
            sleep_time = random.uniform(1, 10)
            time.sleep(sleep_time)
            meta = Item(link)
            items_cat[f"{cat}{indx}"] = {
                "url": link,
                "category": cat,
                "name": meta.get_title(),
                "price": meta.get_price(),
                "image": meta.get_image(),
                "status": meta.get_status(),
                "description": meta.get_description(),
            }
    # ./data/catalog.json
    scrape.write_data_to_file(items_cat, fname_catalog)
    return items_cat


if __name__ == "__main__":
    run_scrape()
