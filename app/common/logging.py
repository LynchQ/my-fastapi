import inspect
import types
from multiprocessing import Lock, Process, Queue
from typing import Any, Dict, List, Optional, Union

import logbook
import orjson
from logbook import Handler, LogRecord, StreamHandler
from logbook.handlers import StringFormatter
from logbook.more import ColorizedStderrHandler

from app.common.constants import LogLevel
from app.conf.settings import settings

logbook.set_datetime_format("local")  # 配置日志时间格式

# lock for creating log process
_log_process_creator_mutex = Lock()


def _log_writer(logger_args, to_ssdb, queue):
    """异步写入日志"""
    # log = Logger(*logger_args, to_ssdb=to_ssdb, async_write=False)
    log = Logger(*logger_args, async_write=False)
    while True:
        log._log(*queue.get())


def _log(self, level, args, kwargs):
    frames = inspect.stack()
    if len(args) > 0 and isinstance(args[0], dict) and len(frames) > 2:
        args[0]["__func"] = frames[2].function
        args[0]["__filename"] = frames[2].filename
        args[0]["__lineno"] = frames[2].lineno

    if not self.async_write:
        return super()._log(level, args, kwargs)  # type: ignore
    else:
        Logger.log_queue.put((level, args, kwargs))


def _default(obj: Any) -> Any:
    if isinstance(obj, set):
        try:
            return sorted(obj)
        except Exception:
            return list(obj)  # sort may fail, e.g. {"abc", 123}

    # just return the string representation for unknown types in logging
    return str(obj)


class JsonFormatter(StringFormatter):
    """Json格式化日志"""

    def __init__(self: "JsonFormatter", format_string: Optional[str] = None, log_context: bool = True) -> None:
        if format_string is None:
            format_string = "[{record.time:%Y-%m-%d %H:%M:%S.%f%z}] {record.level_name}: {record.channel}:"
            if log_context:
                format_string += "{record.base_filename}:{record.lineno}:{record.func_name}"
            format_string += " {record.formatted_message}"
        super().__init__(format_string)

    def _format_message(self: "JsonFormatter", message: Union[str, Dict[Any, Any]]) -> str:
        if isinstance(message, dict):
            message = orjson.dumps(message, default=_default, option=orjson.OPT_SORT_KEYS).decode("utf-8")
        return message

    def format_record(self: "JsonFormatter", record: LogRecord, handler: ColorizedStderrHandler) -> str:
        # 如果日志内容为dict，则将func_name, filename, lineno从dict中取出并赋值给record的对应属性
        if isinstance(record.message, dict):
            if "__func" in record.message:
                record.func_name = record.message.pop("__func")  # 函数名
            if "__filename" in record.message:
                record.filename = record.message.pop("__filename")  # 文件名
                if "__lineno" in record.message:
                    record.lineno = record.message.pop("__lineno")  # 行号
                else:
                    record.lineno = 0  # type: ignore

        record.formatted_message = self._format_message(record.message)  # type: ignore
        record.base_filename = os.path.basename(record.filename)  # type: ignore

        return super().format_record(record, handler)  # type: ignore


class Logger(logbook.Logger):
    def __init__(
        self: "Logger",
        name: Optional[str] = None,  # 日志名称
        level: LogLevel = settings.LOG_LEVEL,  # 日志级别
        colorized_stderr: bool = True,  # 是否在控制台输出彩色日志
        log_file: Optional[str] = None,  # 日志文件路径
        json_format: bool = True,  # 是否以json格式输出日志
        async_write: bool = True,  # 是否异步写入日志
        # to_ssdb: bool = False,  # 是否写入ssdb  TODO
        from_subProcess: bool = False,  # 是否从子进程中写入日志
    ):
        super().__init__(name, logbook.lookup_level(level.value))
        self.handlers: List[Handler]  # for mypy
        if colorized_stderr:
            self.handlers.append(ColorizedStderrHandler(bubble=True))

        if log_file is not None:
            # TODO: not work, fix it
            self.handlers.append(logbook.TimedRotatingFileHandler(log_file, date_format="%Y-%m-%d", bubble=True, encoding="utf-8"))

        if from_subProcess:
            import sys

            self.handlers.append(StreamHandler(sys.stdout))

        if json_format:
            json_formatter = JsonFormatter()
            for handler in self.handlers:
                # TODO: fix it
                handler.formatter = json_formatter  # type: ignore

        self.async_write = async_write
        # 是否异步写入日志 并且 未创建进程
        if self.async_write and not hasattr(Logger, "log_queue"):
            with _log_process_creator_mutex:
                if not hasattr(Logger, "log_queue"):
                    Logger.log_queue = Queue()  # 创建队列
                    # 创建进程
                    Logger.log_process = Process(
                        target=_log_writer,
                        args=(
                            (name, level, colorized_stderr, log_file, json_format),
                            # to_ssdb,
                            Logger.log_queue,
                        ),
                    )
                    Logger.log_process.daemon = True  # daemon 是否为守护进程
                    Logger.log_process.start()  # 启动进程
            self._log = types.MethodType(_log, self)
