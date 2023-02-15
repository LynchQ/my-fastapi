from typing import Dict, Type

from redis.asyncio.client import Redis  # type: ignore
from redis.asyncio.cluster import RedisCluster  # type: ignore
from redis.exceptions import RedisClusterException  # type: ignore

from app.conf import settings


class RedisClient:

    __cache: Dict[str, Redis] = {}

    @classmethod
    async def get_client(cls: Type["RedisClient"], uri: str = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DATABASE}") -> Redis:
        if uri in cls.__cache:
            return cls.__cache[uri]

        try:
            cls.__cache[uri] = RedisCluster.from_url(uri, decode_responses=True)
            await cls.__cache[uri].cluster_info()  # type: ignore
        except RedisClusterException:
            cls.__cache[uri] = Redis.from_url(uri, decode_responses=True)

        return cls.__cache[uri]


if __name__ == "__main__":
    import asyncio

    async def test() -> None:
        client = await RedisClient.get_client("redis://localhost:6379/0")

        print(await client.keys())

    asyncio.get_event_loop().run_until_complete(test())
