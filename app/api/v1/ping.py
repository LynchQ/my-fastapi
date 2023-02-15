from fastapi import APIRouter

from app.common.logging import Logger
from app.schemas.http import ResponseModel

router = APIRouter()
logger = Logger("ping")


@router.get("")
async def ping() -> ResponseModel:
    logger.info({"action": "ping"})
    return ResponseModel(data="pong")
