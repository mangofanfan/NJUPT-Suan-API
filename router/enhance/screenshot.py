"""使用 Playwright 截图"""

from json import dumps
from pathlib import Path
from urllib.parse import urlencode
from uuid import uuid4

from playwright.async_api import ViewportSize

from njupt_api.baselib import PlayContextManager, logger

TEMP_DIR = Path.cwd() / "temp"


class ScreenShot(PlayContextManager):
    def __init__(self) -> None:
        super().__init__()

    async def goto(self, url: str) -> bool:
        await self.page.set_viewport_size(ViewportSize(width=1200, height=900))
        res = await self.page.goto(url)
        logger.debug(f"截图 | {res.ok=} - {url=:.{50}}...")
        return res.ok

    async def shot(self, save_path: str) -> None:
        await self.page.mouse.move(0, 0)
        await self.page.wait_for_load_state("networkidle")
        await self.page.screenshot(path=save_path)
        logger.debug(f"截图 | 截图已经保存在 {save_path=}")
        return


async def generate_img(courses: list[dict], title: str, subtitle: str) -> str:
    """
    方法将生成课程表图片并保存在临时目录中，返回图片的完整名称。图片位于 temp 工作目录。

    Returns:
        字符串，表明生成图片的文件名，格式为 `schedule-{uuid4()}.png`
    """
    t_name = f"schedule-{uuid4()}.png"
    async with ScreenShot() as ss:
        await ss.goto(
            f"127.0.0.1:8000/webui/schedule#/?{
                urlencode({'data': dumps(courses), 'title': title, 'subtitle': subtitle})
            }",
        )
        await ss.shot(str(TEMP_DIR / t_name))
    logger.debug(f"截图 | 生成临时图片 - {t_name}")
    return t_name
