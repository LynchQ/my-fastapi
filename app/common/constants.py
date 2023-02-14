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
