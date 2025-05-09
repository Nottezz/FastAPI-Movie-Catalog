import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_PATH = BASE_DIR / "movie-catalog.json"
LOG_FORMAT = "[-] %(asctime)s [%(levelname)s] %(module)s-%(lineno)d - %(message)s"
LOG_LEVEL = logging.DEBUG

USERS_DB: dict[str, str] = {  # todo: remove
    "sam": "password",
    "bob": "qwerty",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_TOKENS_SET_NAME = "tokens"
