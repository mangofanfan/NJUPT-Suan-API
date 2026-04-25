from datetime import date, timedelta
from typing import Any, Generator, Literal

from pydantic import BaseModel
from sqlmodel import Session

from njupt_suan_api.api.baselib import config

from .alias import apply_alias
from .model import engine
from .screenshot import generate_img


class ScheduleQueryDto(BaseModel):
    username: str | None = None
    password: str | None = None
    week: int = 0
    img: bool = False


class TestDto(BaseModel):
    username: str
    password: str
    scheduleType: Literal["class", "student"]  # noqa: N815


class AliasDto(BaseModel):
    originalName: str  # noqa: N815
    aliasName: str | None  # noqa: N815


class ReturnDto(BaseModel):
    success: bool
    message: str | None = None
    result: Any | None = None
    img_url: str | None = None


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


async def apply_enhance(course_list: list[dict], week: int, img: bool) -> ReturnDto:
    """
    在一个方法中集成了 应用别名 和 生成课表图片 功能。此为异步方法，需要 await。

    Example:
        return await apply_enhance(course_list, week, img)

    Returns:
        返回应用别名和图片完毕的 ReturnDto。
    """
    final_course_list = [course for course in course_list if week in course["weeks"]] if week > 0 else course_list

    final_course_list = apply_alias(final_course_list)

    # 获取课表图片设置
    title_template = config.get("schedule", "schedule_title_template", "芒果酸的课程表")
    subtitle_template = config.get("schedule", "schedule_subtitle_template", "")
    semester_start_date = date.fromisoformat(config.get("schedule", "semester_start_date", "2026-03-02"))

    # 可用变量
    week_start_day = semester_start_date + timedelta(weeks=week)
    vars_ = {
        "week": week,
        "week_start_day": week_start_day.isoformat(),
        "week_end_day": (week_start_day + timedelta(days=6)).isoformat(),
    }

    img_url = None
    if img:
        img_url = f"{config.get('system', 'public_host', 'http://127.0.0.1:8000')}/api/schedule/img/{
            await generate_img(final_course_list, title_template.format(**vars_), subtitle_template.format(**vars_))
        }"

    return ReturnDto(success=True, result=final_course_list, img_url=img_url)
