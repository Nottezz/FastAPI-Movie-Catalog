import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_PATH = BASE_DIR / "movie-catalog.json"
LOG_FORMAT = "[%(levelname)-7s] (%(asctime)s) %(module)s-%(lineno)d: %(message)s"
LOG_LEVEL = logging.DEBUG

API_TOKENS: frozenset[str] = frozenset(  # todo: remove
    {
        "pMZcH1W7lfj86X3aBR7mUg",
        "SYULJUtCQRLyeF2iqt-IGA",
    }
)

USERS_DB: dict[str, str] = {  # todo: remove
    "sam": "password",
    "bob": "qwerty",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
