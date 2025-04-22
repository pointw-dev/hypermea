import redis
import settings

def RedisClient():
    return redis.Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.db
        )
