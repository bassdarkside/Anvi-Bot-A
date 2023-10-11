from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError

fname_pages = "pages.json"
fname_catalog = "catalog.json"
fname_item_pages = "item_pages.json"

URL = "https://anvibodycare.com/"
DESC = ["description", "og:description", "twitter:description"]
TAG = [f"a[href^='{URL}']", "a[href*='.com/shop/']", "a[href*='.com/product']"]
CLASS = [
    "price product-page-price price-on-sale",
    "div[class=woo-product-desc-block]",
    "div[class=product-page-stock-status]",
]
PROXY = {
    "http": "http://188.114.96.76:80",
    # "http": "http://45.8.105.225:80",
    # "http": "http://188.114.96.76:80",
}

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
