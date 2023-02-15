from typing import Generic, Optional, TypeVar

from pydantic.generics import GenericModel

from app.schemas.exceptions import Errors

T = TypeVar("T")


class ResponseModel(GenericModel, Generic[T]):
    code: int = Errors.OK.code
    reason: Optional[str] = Errors.OK.reason
    message: Optional[str] = Errors.OK.message
    data: Optional[T] = None
