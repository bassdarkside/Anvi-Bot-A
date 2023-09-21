from decouple import config
import logging
from logging.handlers import RotatingFileHandler
import telebot


def start_log():
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    file_handler_log = RotatingFileHandler(
        "log/log.txt", maxBytes=1024, backupCount=3
    )
    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler_log.setFormatter(log_formatter)
    telebot.logger.addHandler(file_handler_log)
    chat_log = config("chat_log")


if __name__ == "__main__":
    start_log()
