import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class NoExceptionFilter(logging.Filter):
    def filter(self, record):
        record.exc_info = None
        record.exc_text = None
        return True


def config_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists("logs/error"):
        os.makedirs("logs/error")

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Console handler for ERROR level logs
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

    # File handler for INFO level logs with size-based rotation
    file_handler_info = RotatingFileHandler(
        filename="logs/info.log", mode="a", maxBytes=10485760, backupCount=5  # 10 MB  # Keep 5 backup files
    )
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler_info)

    # File handler for ERROR level logs with daily rotation and separate files for each date
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_handler_error = TimedRotatingFileHandler(
        filename=f"logs/error/error_{today_date}.log",  # Include date in the filename
        when="midnight",
        interval=1,
        backupCount=7,  # Keep logs for last 7 days
    )
    file_handler_error.setLevel(logging.ERROR)
    file_handler_error.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler_error)
