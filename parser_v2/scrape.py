import json
import requests as req
from pathlib import Path
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
import traceback

path = Path(__file__)
path = path.parent.joinpath("data")


class Scrape:
    def __init__(self, url):
        self.url = url
        if self.url is None:
            raise ValueError("url is None.")

    def soup(self):
        try:
            user_agent = UserAgent().random
        except FakeUserAgentError as e:
            print(e)
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
            "User-Agent": user_agent,
        }
        response = req.get(self.url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            soup = None
        return soup

    def write_data_to_file(self, data, filename):
        with open(f"{path}/{filename}.py", mode="w", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("write OK")

    def all_urls(self, write=False):
        links_data = self.soup().select("a[href^='https']")
        links = []
        for link in links_data:
            link = link.get("href")
            if link not in links:
                # if we dont need facebook links
                if "facebook" in link:
                    continue
                links.append(link)
        if write:
            # filename as name of function
            filename = traceback.extract_stack(None, 2)[1][2]
            self.write_data_to_file(links, filename)
        return links
