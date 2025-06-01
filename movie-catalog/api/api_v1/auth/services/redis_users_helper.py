__all__ = ["redis_users"]
from redis import Redis
from typing import cast

from .users_helper import AbstractUsersHelper
from config import REDIS_HOST, REDIS_PORT, REDIS_DB_USERS


class RedisUsersHelper(AbstractUsersHelper):
    def __init__(self, host: str, port: int, db: int) -> None:
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

    def get_user_password(self, username: str) -> str | None:
        return self.redis.get(username)


redis_users = RedisUsersHelper(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_USERS)
