from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = [
    "IntIDPrimaryKeyMinxin",
    "UUIDPrimaryKeyMinxin",
    "CreatedAtMixin",
    "UpdatedAtMixin",
]


class IntIDPrimaryKeyMinxin(BaseModel):
    id: int = Field(pk=True, description="主键ID")


class UUIDPrimaryKeyMinxin(BaseModel):
    id: UUID = Field(pk=True, description="主键ID")


class CreatedAtMixin(BaseModel):
    created_at: datetime = Field(..., description="创建时间")


class UpdatedAtMixin(BaseModel):
    updated_at: datetime = Field(..., description="更新时间")
