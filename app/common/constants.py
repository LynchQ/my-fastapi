from enum import Enum

import logbook


class LogLevel(int, Enum):
    Critical = logbook.CRITICAL
    Error = logbook.ERROR
    Warning = logbook.WARNING
    Notice = logbook.NOTICE
    Info = logbook.INFO
    Debug = logbook.DEBUG
    Trace = logbook.TRACE
    NotSet = logbook.NOTSET


class UserStatus(str, Enum):
    """用户状态: 未验证 -> 启用 -> 禁用"""

    NotVerified = "NotVerified"
    Active = "Active"
    Inactive = "Inactive"
