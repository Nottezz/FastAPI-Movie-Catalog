import logging
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class LoggingConfig(BaseModel):
    log_format: str = (
        "[-] %(asctime)s [%(levelname)s] %(module)s-%(lineno)d - %(message)s"
    )
    log_level_name: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "WARNING"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisDatabaseConfig(BaseModel):
    default: int = 0
    tokens: int = 1
    users: int = 2
    movie_catalog: int = 3

    @model_validator(mode="after")
    def validate_dbs_numbers_unique(self) -> Self:
        db_value = list(self.model_dump().values())
        if len(set(db_value)) != len(db_value):
            raise ValueError("Database numbers must have unique values")
        return self


class RedisCollectionsNamesConfig(BaseModel):
    tokens_set: str = "tokens"
    movie_catalog_hash: str = "movie_catalog"


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDatabaseConfig = RedisDatabaseConfig()
    collections: RedisCollectionsNamesConfig = RedisCollectionsNamesConfig()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",
        ),
        env_prefix="MOVIE_CATALOG__",
        env_nested_delimiter="__",
    )

    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
