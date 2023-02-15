from typing import Any, Dict, List, Union

from fastapi import status
from pydantic import BaseModel, Field


class Error(BaseModel):
    code: int = Field(None, example=status.HTTP_400_BAD_REQUEST, description="具体错误代码")
    reason: str = Field(None, example="Bad Request", description="错误原因名称")
    message: str = Field(None, example="The request is invalid.", description="错误信息, 用于展示")
    http_status: int = Field(status.HTTP_400_BAD_REQUEST, example=status.HTTP_400_BAD_REQUEST, description="http 状态码")

    def __eq__(self: "Error", other: object) -> bool:
        return isinstance(other, Error) and self.code == other.code and self.reason == other.reason

    def __hash__(self: "Error") -> int:
        return hash((self.code, self.reason, self.http_status))

    def __lt__(self: "Error", other: "Error") -> bool:
        return (self.http_status, self.code, self.reason) < (other.http_status, other.code, other.reason)


class Errors:
    OK = Error(code=0, reason="OK", message="OK", http_status=status.HTTP_200_OK)
    UNKNOWN = Error(code=99999999, reason="UNKNOWN", message="未知错误", http_status=status.HTTP_400_BAD_REQUEST)
    REQUEST_VALIDATION_ERROR = Error(code=99990001, reason="REQUEST_VALIDATION_ERROR", message="请求参数校验错误", http_status=status.HTTP_400_BAD_REQUEST)

    BAD_REQUEST = Error(code=400, reason="BAD REQUEST", message="请求参数错误", http_status=status.HTTP_400_BAD_REQUEST)
    UNAUTHORIZED = Error(code=401, reason="UNAUTHORIZED", message="身份验证凭证校验失败", http_status=status.HTTP_401_UNAUTHORIZED)
    FORBIDDEN = Error(code=403, reason="FORBIDDEN", message="权限不足", http_status=status.HTTP_403_FORBIDDEN)
    NOT_FOUND = Error(code=404, reason="NOT FOUND", message="资源不存在", http_status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def E(code: int, reason: str, message: str, http_status: int = status.HTTP_400_BAD_REQUEST) -> Error:
        return Error(code=code, reason=reason, message=message, http_status=http_status)


class HTTPException(Exception):
    def __init__(self: "HTTPException", error: Error, *args: List[Any]) -> None:
        super().__init__(*args)
        self.error: Error = error


HTTP_STATUS: Dict[int, str] = {getattr(status, status_name): status_name for status_name in dir(status) if status_name.startswith("__")}


def response_errors(*errors: Error) -> Dict[Union[int, str], Dict[str, Any]]:
    responses: Dict[Union[int, str], Dict[str, Any]] = {}
    for e in sorted(list(set(errors))):
        if e.http_status not in responses:
            responses[e.http_status] = {
                "description": HTTP_STATUS.get(e.http_status, "UNKNOWN"),
                "content": {"application/json": {"examples": {}}},
            }
        responses[e.http_status]["content"]["application/json"]["examples"][e.reason] = {
            "summary": f"{e.message} ({e.code}:{e.reason})",
            "value": {
                "code": e.code,
                "reason": e.reason,
                "message": e.message,
            },
        }

    return responses


if __name__ == "__main__":
    responses = response_errors(
        Errors.E(10001002, "USERNAME_TOO_SHORT", "用户名至少需要4个字符"),
        Errors.E(10001000, "USER_ALREADY_EXISTS", "用户已存在"),
    )

    print(responses)
