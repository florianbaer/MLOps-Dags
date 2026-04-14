import coloredlogs
import logging

LOG_LEVEL = logging.INFO

def get_logger(name: str):
    logger = logging.getLogger(name)
    coloredlogs.install(level="DEBUG", logger=logger)
    logger.setLevel(LOG_LEVEL)
    return logger
