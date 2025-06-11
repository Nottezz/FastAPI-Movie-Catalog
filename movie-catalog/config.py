import logging
from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_PATH = BASE_DIR / "movie-catalog.json"
LOG_FORMAT = "[-] %(asctime)s [%(levelname)s] %(module)s-%(lineno)d - %(message)s"
LOG_LEVEL = logging.DEBUG

REDIS_HOST = "localhost"
REDIS_PORT = int(getenv("RADIS_PORT", 0)) or 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2
REDIS_DB_MOVIE_CATALOG = 3
REDIS_TOKENS_SET_NAME = "tokens"
REDIS_MOVIE_CATALOG_HASH_NAME = "movie-catalog"
