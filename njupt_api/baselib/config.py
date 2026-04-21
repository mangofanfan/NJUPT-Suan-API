from json import dumps, loads
from pathlib import Path
from typing import TypeVar

import aiofiles

from .logger import logger

CONFIG_PATH = Path.cwd() / "data" / "config.json"


T = TypeVar("T")


class Config:
    def __init__(self) -> None:
        self._doc = {}

    async def load_json(self) -> None:
        """
        从 Toml 配置文件中读取配置。
        """
        logger.debug("异步读取配置文件。")
        async with aiofiles.open(file=CONFIG_PATH, mode="r") as f:
            self._doc = loads(await f.read())

    def sync_load_json(self) -> None:
        """
        同步读取配置文件，仅限于 main.py 中启动时。

        Raises:
            FileNotFoundError: 配置文件不存在。
        """
        logger.debug("同步读取配置文件。")
        try:
            with open(file=CONFIG_PATH, mode="r") as f:
                self._doc = loads(f.read())
        except FileNotFoundError:
            logger.warning("FileNotFoundError - 配置文件不存在。")
            raise

    def sync_create_json(self) -> None:
        """
        同步创建配置文件。
        """
        logger.debug("同步创建配置文件。")
        with open(file=CONFIG_PATH, mode="w") as f:
            f.write(dumps(self._doc))

    def init_config(self) -> None:
        """
        重新初始化 Toml 配置文件。这会重置所有配置。
        """
        logger.warning("初始化配置文件，这会重置所有配置。")
        self._doc.clear()
        doc_system = {}
        doc_schedule = {}
        doc_log = {}

        doc_system["host"] = "0.0.0.0"
        doc_system["port"] = 8000
        doc_system["reload"] = True

        doc_schedule["playwright_headless"] = True
        doc_schedule["jwxt_login_method"] = "sso"
        doc_schedule["semester_start_date"] = "2026-03-02"
        doc_schedule["schedule_title_template"] = "芒果酸的第 {title} 周课程表"
        doc_schedule["schedule_subtitle_template"] = "我也要上吗？"

        doc_log["log_api_request_details"] = False
        doc_log["log_mcp_request_details"] = False
        doc_log["log_assets_request"] = False

        self._doc["system"] = doc_system
        self._doc["schedule"] = doc_schedule
        self._doc["log"] = doc_log

    async def save_json(self) -> None:
        """
        异步保存 Toml 配置文件。
        """
        logger.debug("异步保存配置文件。")
        async with aiofiles.open(file=CONFIG_PATH, mode="w") as f:
            await f.write(dumps(self._doc, indent=4))

    def get(self, group: str, option: str, default: T) -> T:
        """
        获取配置项的值。

        Args:
            group: Table
            option: Key
            default: 默认值

        Returns:
            Any，与 default 参数类型相同。
        """
        try:
            return self._doc.get(group).get(option)
        except AttributeError:
            return default

    def to_dict(self) -> dict:
        return self._doc

    def from_dict(self, data: dict) -> None:
        self._doc.clear()
        for key, value in data.items():
            if isinstance(value, dict):
                t_table = {}
                for k, v in value.items():
                    t_table[k] = v
                self._doc[key] = t_table


config = Config()
