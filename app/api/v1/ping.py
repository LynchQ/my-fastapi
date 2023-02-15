from fastapi import APIRouter

from app.common.logging import Logger

router = APIRouter()
logger = Logger("ping")


@router.get("")
async def ping() -> dict:
    logger.info({"action": "ping"})
    return {"code": "200", "reason": "", "message": "pong", "data": ""}
