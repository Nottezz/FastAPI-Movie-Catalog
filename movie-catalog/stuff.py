from redis import Redis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def main():
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
