"""为课程提供一个简短的别名，便于在空间有限的课程表图片中辨认。

别名是单独保存的，在最终输出阶段才会被装饰在原有的课表输出上。
"""

from typing import Sequence

from sqlmodel import Session, select

from njupt_api.baselib import logger
from router.enhance.model import Alias, engine


def apply_alias(courses: list[dict]) -> list[dict]:
    with Session(engine) as session:
        aliases: Sequence[Alias] = session.exec(select(Alias)).all()

        # 否则不做任何更改
        if len(aliases) == 0:
            return courses

    alias_count = 0
    apply_count = 0

    alias_dict = {}
    for alias in aliases:
        m = alias.model_dump()
        alias_dict[m["originalName"]] = m["aliasName"]
        alias_count += 1

    for course in courses:
        if course["name"] in alias_dict:
            course["alias"] = alias_dict[course["name"]]
            apply_count += 1
        else:
            course["alias"] = None

    logger.debug(
        f"课程别名 | 将 {alias_count} 个别名应用在了 {apply_count} 门输出的课程上。",
    )
    return courses
