from typing import Dict, Optional

from redis.asyncio.client import Redis  # type: ignore

from app.conf import settings

# from redis.asyncio.cluster import RedisCluster  # type: ignore
# from redis.exceptions import RedisClusterException  # type: ignore


# class RedisClient:

#     __cache: Dict[str, Redis] = {}

#     @classmethod
#     async def get_client(cls: Type["RedisClient"], uri: str = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DATABASE}") -> Redis:
#         if uri in cls.__cache:
#             return cls.__cache[uri]

#         try:
#             cls.__cache[uri] = RedisCluster.from_url(uri, decode_responses=True)
#             await cls.__cache[uri].cluster_info()  # type: ignore
#         except RedisClusterException:
#             cls.__cache[uri] = Redis.from_url(uri, decode_responses=True)

#         return cls.__cache[uri]

RedisClient: Dict[int, Redis] = {
    db: Redis.from_url(
        f"{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        db=db,
        max_connections=10,
        encoding="utf-8",
        decode_responses=True,
    )
    for db in range(0, 16)
}

# 验证码使用的redis
img_code_redis: Optional[Redis] = RedisClient.get(0)
sms_code_redis: Optional[Redis] = RedisClient.get(1)

# user 使用的redis
user_info_redis: Optional[Redis] = RedisClient.get(2)


if __name__ == "__main__":
    import asyncio

    async def test() -> None:
        if user_info_redis:
            async with user_info_redis.pipeline(transaction=True) as pipe:
                pipe.keys()

    asyncio.get_event_loop().run_until_complete(test())
