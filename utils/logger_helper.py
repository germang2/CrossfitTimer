import logging

from utils.contants import (
    APP_PATH
)

logging.basicConfig(
    filename=f"{APP_PATH}/logger.log",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    datefmt="%Y-%m-%d %H:%M",
    style="{",
)

logger = logging.getLogger()