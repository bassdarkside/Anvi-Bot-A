from scrape import Scrape
from config import URL

scrape = Scrape(URL)
result = scrape.all_urls(write=False)
print(result)
