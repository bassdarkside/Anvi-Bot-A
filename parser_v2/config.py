from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
from pathlib import Path

PAGES = "pages.json"
ITEMS = "items.json"
CATALOG = "catalog.json"

URL = "https://anvibodycare.com/"

DATAPATH = Path(__file__).parent.joinpath("data")

TAG = [f"a[href^='{URL}']", "a[href*='.com/shop/']", "a[href*='.com/product']"]

try:
    user_agent = UserAgent().random
except FakeUserAgentError as e:
    print(e)

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "Accept-Language": "*",
    "Accept-Encoding": "*",
    "Referer": "https://www.google.com/",
    "User-Agent": user_agent,
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Connection": "keep-alive",
}

PROXY = {
    "http": "http://188.114.96.76:80",
    # "http": "http://45.8.105.225:80",
    # "http": "http://188.114.96.76:80",
}
