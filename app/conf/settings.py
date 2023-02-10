from functools import lru_cache
from typing import List

from pydantic import BaseSettings

from app.utils.env import Env


class Settings(BaseSettings):
    # 基础信息
    TITLE: str = "MyFastAPI"
    VERSION: str = "v0.0.1"
    DESCRIPTION: str = ""
    URL_PREFIX: str = "/api"
    DOCS_URL = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    DEBUG: bool = Env.boolean(name="DEBUG", default=False, description="是否开启调试模式")

    # 数据库(使用的MySQL)
    DB_HOST: str = Env.string(name="DB_HOST", default="127.0.0.1", description="数据库地址", contains_secret=True)
    DB_PORT: int = Env.int(name="DB_PORT", default=3306, description="数据库端口", contains_secret=True)
    DB_USER: str = Env.string(name="DB_USER", default="root", description="数据库用户名", contains_secret=True)
    DB_PASSWORD: str = Env.string(name="DB_PASSWORD", default="123456", description="数据库密码", contains_secret=True)
    DB_DATEBASE: str = Env.string(name="DB_DATEBASE", default="myfastapi", description="数据库名称", contains_secret=True)
    DB_ENCODING: str = "utf8mb4"

    # Redis
    REDIS_HOST: str = Env.string(name="REDIS_HOST", default="127.0.0.1", description="Redis host", contains_secret=True)
    REDIS_PORT: int = Env.int(name="REDIS_PORT", default=6379, description="Redis port", contains_secret=True)
    REDIS_PASSWORD: str = Env.string(name="REDIS_PASSWORD", default="", description="Redis password", contains_secret=True)
    REDIS_DATABASE: int = Env.int(name="REDIS_DATABASE", default=0, description="Redis database", contains_secret=True)
    REDISTIMEOUT: int = Env.int(name="REDISTIMEOUT", default=60, description="Redis timeout")

    # Elasticsearch
    ELASTICSEARCH_HOSTS: List[str] = Env.json(name="ELASTICSEARCH_HOSTS", default=["http://localhost:9200"], description="Elasticsearch hosts")

    # JWT
    JWT_TOKEN_PREFIX: str = "MyFastAPI"
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_SECRET_KEY: str = "123456"

    # 中间件
    ALLOW_ORIGINS: List[str] = Env.json(name="ALLOW_ORIGINS", default=["*"], description="允许跨域的域名")


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
