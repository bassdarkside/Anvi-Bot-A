from .scrape import Scrape, Item
from .config import URL


def run_scrape():
    """
    The `run` function scrapes product information from a website,
    stores it in a dictionary, and writes it to a JSON file.

    :return: The function `run()` is returning a dictionary `items_cat`
    which contains information aboutthe scraped items.

    Path file 'parser_v2/data/catalog.json'
    """
    scrape = Scrape()
    scrape.get_urls(URL, write=False)
    item_urls = scrape.get_products_urls(write=True)
    items_cat = {}
    for indx, link in enumerate(item_urls, start=1):
        meta = Item(link)
        items_cat[indx] = {
            "name": meta.get_title(),
            "chapter": "chapter",
            "price": meta.get_price(),
            "url": link,
            "description": meta.get_description(),
            "image": meta.get_image(),
        }

    # ./data/catalog.json
    scrape.write_data_to_file(items_cat, "catalog")
    return items_cat


if __name__ == "__main__":
    run_scrape()
