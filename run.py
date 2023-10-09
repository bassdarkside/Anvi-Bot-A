from parser_v2.main import scrape_url, make_catalog
from bot_start.logger_run import start_logging
from bot_start.bot_initial import bot_run


if __name__ == "__main__":
    scrape_url()
    make_catalog()
    # start_logging()
    bot_run()
