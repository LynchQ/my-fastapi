from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def ping() -> dict:
    return {"code": "200", "reason": "", "message": "pong", "data": ""}
