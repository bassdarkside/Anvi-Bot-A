from pathlib import Path
from logging.handlers import RotatingFileHandler
import logging
import telebot

folder_path = Path(__file__).parent.parent
folder_path = str(folder_path) + "/log"


def start_logging():
    """
    The function `start_logging()` creates a log folder if it
        doesn't exist, sets the logging level to ERROR,
        and adds a file handler to log messages to a file.
    """
    if not Path(folder_path).exists():
        Path(folder_path).mkdir()
        print("Folder '/log' was created.")

    telebot.logger.setLevel(logging.ERROR)
    file_handler_log = RotatingFileHandler(
        f"{folder_path}/bot_log.txt", maxBytes=1024, backupCount=3
    )
    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler_log.setFormatter(log_formatter)
    telebot.logger.addHandler(file_handler_log)
    print("Logging is started..")


if __name__ == "__main__":
    start_logging()
