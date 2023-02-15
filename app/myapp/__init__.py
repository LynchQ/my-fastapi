from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.common.logging import Logger
from app.conf.settings import settings
from app.db.sql import BASE_TORTOISE_ORM

logger = Logger("myapp")


def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.TITLE,  # 标题
        description=settings.DESCRIPTION,  # 描述
        version=settings.VERSION,  # 版本
        docs_url=settings.DOCS_URL,  # 文档地址
        redoc_url=settings.REDOC_URL,  # 文档地址
        openapi_url=settings.OPENAPI_URL,  # 文档地址
    )
    logger.info({"docs_url": f"http://0.0.0.0:8000/{settings.DOCS_URL}"})  # 打印些提示到日志

    # 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 异常处理
    @app.exception_handler(Exception)
    async def common_exception_handler(request: Request, e: Exception) -> JSONResponse:
        logger.exception(e)
        return JSONResponse(
            content={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "MyAPI Internal Server Error",
                "reason": f"{e.args}",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # 数据库
    torroise_orm = BASE_TORTOISE_ORM
    app.torroise_orm = torroise_orm  # type: ignore

    return app
