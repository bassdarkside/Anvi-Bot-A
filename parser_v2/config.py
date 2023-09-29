from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError

URL = "https://www.anvibodycare.com"
TAG = ["a[href^='https://www.anvibodycare.com/']", "a[href*='.com/pr']"]
PROP = ["product:price:amount", "span[data-wix-price]"]
DESC = ["description", "og:description", "twitter:description"]

try:
    user_agent = UserAgent().random
except FakeUserAgentError as e:
    print(e)

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": user_agent,
}
