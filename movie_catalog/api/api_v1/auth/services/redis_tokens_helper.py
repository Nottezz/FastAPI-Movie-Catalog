__all__ = ["redis_tokens"]

from redis import Redis

from movie_catalog.api.api_v1.auth.services.tokens_helper import AbstractTokensHelper
from movie_catalog.config import (
    REDIS_DB_TOKENS,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_TOKENS_SET_NAME,
)


class RedisTokensHelper(AbstractTokensHelper):

    def __init__(self, host: str, port: int, db: int, tokens_set_name: str) -> None:
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)
        self.tokens_set = tokens_set_name

    def token_exists(self, token: str) -> bool:
        return bool(self.redis.sismember(self.tokens_set, token))

    def add_token(self, token: str) -> None:
        self.redis.sadd(self.tokens_set, token)

    def get_tokens(self) -> list[str]:
        return list(self.redis.smembers(self.tokens_set))

    def delete_token(self, token: str) -> None:
        self.redis.srem(self.tokens_set, token)


redis_tokens = RedisTokensHelper(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB_TOKENS,
    tokens_set_name=REDIS_TOKENS_SET_NAME,
)
