import redis
from .redis_client import RedisClient

def get_redis_client():
    return RedisClient()
