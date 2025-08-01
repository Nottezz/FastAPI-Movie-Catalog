__all__ = ["redis_users"]

from config import settings
from redis import Redis

from .users_helper import AbstractUsersHelper


class RedisUsersHelper(AbstractUsersHelper):
    def __init__(self, host: str, port: int, db: int) -> None:
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

    def get_user_password(self, username: str) -> str | None:
        return self.redis.get(username)


redis_users = RedisUsersHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.users,
)
