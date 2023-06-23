import redis
import os


def get_redis_db():
    redis_url = os.environ.get("REDIS_URL", "localhost")
    return redis.Redis(host=redis_url, port=6379, decode_responses=True)
