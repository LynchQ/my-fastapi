from typing import Any, Dict, Final

from app.conf import settings

DB_CONN_STR: Final = f"mysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATEBASE}?pool_recycle=21600?charset={settings.DB_ENCODING}"
BASE_TORTOISE_ORM: Dict[str, Any] = {
    "connections": {"default": DB_CONN_STR},
    "routers": ["default"],
    "use_tz": True,
    "timezone": "Asia/Shanghai",
}
