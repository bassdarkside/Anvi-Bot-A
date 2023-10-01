from pathlib import Path
from logging.handlers import RotatingFileHandler
import logging
import telebot


def start_logging():
    """
    The function `start_logging()` creates a log folder if it
        doesn't exist, sets the logging level to ERROR,
        and adds a file handler to log messages to a file.
    """
    folder_path = "Anvi-Bot-A/log"

    if not Path(folder_path).exists():
        Path(folder_path).mkdir()
        print(f"Folder '{folder_path}' was created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

    telebot.logger.setLevel(logging.ERROR)

    file_handler_log = RotatingFileHandler(
        f"{folder_path}/bot_log.txt", maxBytes=1024, backupCount=3
    )
    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler_log.setFormatter(log_formatter)
    telebot.logger.addHandler(file_handler_log)


if __name__ == "__main__":
    start_logging()
