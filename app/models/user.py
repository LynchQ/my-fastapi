from tortoise import fields
from tortoise.models import Model

from app.common import constants
from app.models.base import CreatedAtMixin, UpdatedAtMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, CreatedAtMixin, UpdatedAtMixin, Model):
    username = fields.CharField(min_length=4, max_length=255, null=False, unique=True, index=True, description="用户名")
    password = fields.CharField(max_length=128, null=False, description="密码")
    status = fields.CharEnumField(enum_type=constants.UserStatus, description="用户状态")
    nickname = fields.CharField(max_length=255, null=True, description="昵称")
    email = fields.CharField(max_length=255, null=True, description="邮箱")
    mobile = fields.CharField(max_length=255, null=True, description="手机号")
    avatar = fields.CharField(max_length=255, null=True, default="", description="头像")

    class Meta:
        table = "my_app__user"  # 指定模型映射的数据库表名
        # db_table = "my_app__user" # 指定模型映射的数据库表名，优先级高于 table
        table_description = "用户表"  # 指定数据库表的描述
        unique_together = ("username", "email", "mobile")  # 联合唯一约束
        indexes = ["username", "email", "mobile"]  # 索引
        ordering = ["-created_at"]  # 排序 默认升序
        # tablespace = "pg_default"  # 表空间

    def __str__(self):
        return f"User(id={self.id}, username={self.username}, nickname={self.nickname})"
