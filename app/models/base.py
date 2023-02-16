from tortoise import fields
from tortoise.models import Model


class IntIDPrimaryKeyMixin(Model):
    id = fields.IntField(pk=True, description="主键ID int类型")


class UUIDPrimaryKeyMixin(Model):
    id = fields.UUIDField(pk=True, description="主键ID uuid类型")


class CreatedAtMixin(Model):
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")


class UpdatedAtMixin(Model):
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")


class IsDeletedMixin(Model):
    is_deleted = fields.BooleanField(null=False, default=False, description="是否删除")
