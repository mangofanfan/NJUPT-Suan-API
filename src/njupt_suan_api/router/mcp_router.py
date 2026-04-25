from pathlib import Path
from typing import Annotated

from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import ToolAnnotations
from pydantic import Field
from sqlmodel import Session, select

from njupt_suan_api.api.baselib import LoggingMiddleware, logger
from njupt_suan_api.api.zhengfang import LoginError, course_dict_serializer, course_list_serializer, jwxt
from njupt_suan_api.router.enhance.lib import ReturnDto, apply_enhance
from njupt_suan_api.router.enhance.model import Course, engine

mcp = FastMCP("NJUPT API Suan")

mcp.add_middleware(LoggingMiddleware())

mcp_app = mcp.http_app("/")


# 统一参数文档
USERNAME_TYPE = Annotated[str, Field(description="用户名，也即学号，一般是一位字母接八位数字，字母需要大写。")]
PASSWORD_TYPE = Annotated[str, Field(description="密码，字符串。")]
WEEK_TYPE = Annotated[int, Field(description="获取第几周的课表，默认为 0 即获取全部。")]
IMG_TYPE = Annotated[
    bool,
    Field(
        description="是否需要同时生成图片，默认为 False。如果为 True，图片链接将在 img_url 中提供，链接有效时间为两小时。",  # noqa: E501
    ),
]


@mcp.tool(
    name="tool_schedule_class",
    title="获取默认班级课表",
    description="获取存储在酸 API 中的默认班级课表，返回值包含 success result message 和 img_url 四个字段。",
    annotations=ToolAnnotations(
        title="获取默认课表",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
async def tool_schedule_class(
    week: WEEK_TYPE = 0,
    img: IMG_TYPE = False,
) -> ReturnDto:
    with Session(engine) as session:
        course_dtos = session.exec(select(Course)).all()
    logger.success("从数据库中返回一次性存储的班级课表。")
    course_list: list[dict] = [course_dict_serializer(course) for course in course_dtos]
    return await apply_enhance(course_list, week, img)


@mcp.tool(
    name="tool_schedule_class_special",
    title="获取指定学生的班级课表",
    description="获取指定学生的班级课表。需要提供学号和密码。返回值包含 success result message 和 img_url 四个字段。",
    annotations=ToolAnnotations(
        title="获取指定学生的班级课表",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
async def tool_schedule_class_special(
    username: USERNAME_TYPE,
    password: PASSWORD_TYPE,
    week: WEEK_TYPE = 0,
    img: IMG_TYPE = False,
) -> ReturnDto:
    try:
        async with jwxt(username, password) as zf:
            final_course_list = course_list_serializer(await zf.get_class_schedule())
            logger.success(f"{username} | 获取指定学生的班级课表成功。")
            return await apply_enhance(final_course_list, week, img)
    except LoginError as e:
        return ReturnDto(success=False, message=str(e))


@mcp.tool(
    name="tool_schedule_student_special",
    title="获取指定学生的个人课表",
    description="获取指定学生的个人课表。需要提供学号和密码。返回值包含 success result message 和 img_url 四个字段。",
    annotations=ToolAnnotations(
        title="获取指定学生的个人课表",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
async def tool_schedule_student_special(
    username: USERNAME_TYPE,
    password: PASSWORD_TYPE,
    week: WEEK_TYPE = 0,
    img: IMG_TYPE = False,
) -> ReturnDto:
    try:
        async with jwxt(username, password) as zf:
            final_course_list = course_list_serializer(await zf.get_student_schedule())
            logger.success(f"{username} | 获取指定学生的个人课表成功。")
            return await apply_enhance(final_course_list, week, img)
    except LoginError as e:
        return ReturnDto(success=False, message=str(e))


@mcp.tool(
    name="tool_schedule_image",
    title="直接获取课表图片",
    description="接收使用其他课表工具得到的图片的文件名，返回 ImageContent。",
    annotations=ToolAnnotations(
        title="直接获取课表图片",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
async def tool_schedule_image(
    img_name: Annotated[str, Field(description="课表图片的文件名，形如 schedule-{uuid4}.png")],
) -> Image | ReturnDto:
    img_path = Path.cwd() / "temp" / img_name
    if img_path.exists():
        return Image(path=img_path)
    return ReturnDto(success=False, message=f"未找到指定的课表图片 {img_name}")
