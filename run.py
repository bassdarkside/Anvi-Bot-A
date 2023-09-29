from parser_v2.main import run_scrape
from bot_start.bot_initial import bot_run

"""
The main function runs a web scraping process and then starts a bot.
:return:    The `catalog_` variable is being
            returned from the `main()` function.
"""


def main():
    catalog_ = run_scrape()
    return catalog_


if __name__ == "__main__":
    main()
    bot_run()
