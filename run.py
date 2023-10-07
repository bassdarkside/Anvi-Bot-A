from parser_v2.main import make_catalog, scrape_url
from bot_start.bot_initial import bot_run
from bot_start.logger_run import start_logging  # .

"""
The main function runs a web scraping process and then starts a bot.
:return:    The `catalog_` variable is being
            returned from the `main()` function.
"""


def parser_prepare():
    scrape_url()


def get_catalog():
    catalog_ = make_catalog()
    return catalog_


def bot():
    start_logging()
    bot_run()


if __name__ == "__main__":
    parser_prepare()
    get_catalog()
    bot()
