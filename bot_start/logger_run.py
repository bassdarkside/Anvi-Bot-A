import socket
import logging
from logging.handlers import SysLogHandler
import telebot


def start_logging():
    """Send log to "https://papertrailapp.com" """
    print("Logging is started..")

    class ContextFilter(logging.Filter):
        hostname = socket.gethostname()

        def filter(self, record):
            record.hostname = ContextFilter.hostname
            return True

    syslog = SysLogHandler(address=("logs6.papertrailapp.com", 20102))
    syslog.addFilter(ContextFilter())

    format = "%(asctime)s - %(hostname)s - %(message)s"
    log_formatter = logging.Formatter(format, datefmt="%b %d %H:%M:%S")

    syslog.setFormatter(log_formatter)
    telebot.logger.addHandler(syslog)
    telebot.logger.setLevel(logging.ERROR)


if __name__ == "__main__":
    start_logging()
