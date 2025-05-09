from redis import Redis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB_TOKENS

redis_tokens = Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_TOKENS, decode_responses=True
)
