import sys
from collections import deque

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    level="DEBUG",
    colorize=True,
)
logger.add("data/app.log", rotation="10 MB", retention="7 days")  # 文件日志

log_buffer = deque(maxlen=1000)


class LogRecord:
    log_counter = 0

    def __init__(self, message: str) -> None:
        self.id = LogRecord.log_counter
        self.message = message

        LogRecord.log_counter += 1


def log_record_serialize(record: LogRecord) -> dict:
    return {
        "id": record.id,
        "message": record.message,
    }


def memory_sink(message: str) -> None:
    """向自定义缓冲区写入日志，供 WebUI 获取
    :param message: 'loguru._handler.Message'
    """
    log_entry = LogRecord(message=message)
    log_buffer.append(log_entry)


logger.add(sink=memory_sink, level="DEBUG", colorize=True)
