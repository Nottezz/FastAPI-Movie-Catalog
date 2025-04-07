import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE_PATH = BASE_DIR / "movie-catalog.json"
LOG_FORMAT = "[%(levelname)s] (%(asctime)s) %(module)s-%(lineno)d: %(message)s"
LOG_LEVEL = logging.INFO
