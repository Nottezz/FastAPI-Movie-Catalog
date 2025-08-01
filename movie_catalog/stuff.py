from config import settings
from redis import Redis

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.default,
    decode_responses=True,
)


def main() -> None:
    print(redis.ping())
    print(redis.info())
    redis.set("name", "Nikita")
    print("name", redis.get("name"))
    redis.set("foo", "bar")
    redis.set("number", "42")
    print([redis.get("foo"), redis.get("number"), redis.get("spam")])
    redis.delete("name")
    print("name", redis.get("name"))


if __name__ == "__main__":
    main()
