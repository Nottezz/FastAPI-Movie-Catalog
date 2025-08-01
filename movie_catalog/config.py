import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class LoggingConfig(BaseModel):
    log_format: str = (
        "[-] %(asctime)s [%(levelname)s] %(module)s-%(lineno)d - %(message)s"
    )
    log_level: int = logging.DEBUG
    log_date_format: str = "%Y-%m-%d %H:%M:%S"


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisDatabaseConfig(BaseModel):
    default: int = 0
    tokens: int = 1
    users: int = 2
    movie_catalog: int = 3


class RedisCollectionsNamesConfig(BaseModel):
    tokens_set: str = "tokens"
    movie_catalog_hash: str = "movie_catalog"


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDatabaseConfig = RedisDatabaseConfig()
    collections: RedisCollectionsNamesConfig = RedisCollectionsNamesConfig()


class Settings(BaseSettings):
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
