import logbook

logbook.set_datetime_format("local")  # 配置日志时间格式

class Logger(logbook.Logger):
    ...