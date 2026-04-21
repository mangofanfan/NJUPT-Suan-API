from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from njupt_api.baselib import logger
from njupt_api.zhengfang import (
    course_dict_serializer,
    course_list_serializer,
    jwxt,
)
from njupt_api.zhengfang.exc import LoginError
from router.enhance.lib import ReturnDto, ScheduleQueryDto, apply_enhance, get_session
from router.enhance.model import Course

TEMP_DIR = Path.cwd() / "temp"


api_router = APIRouter(prefix="/api", tags=["API"])


@api_router.post("/schedule/class")
async def post_schedule_class(
    student: ScheduleQueryDto,
    session: Annotated[Session, Depends(get_session)],
) -> ReturnDto:
    if student.username is None and student.password is None:
        logger.debug("未提供学号和密码参数，尝试从数据库中返回一次性存储的班级课表。")
        course_dtos = session.exec(select(Course)).all()
        course_list: list[dict] = [course_dict_serializer(course) for course in course_dtos]
        logger.success(f"{student.week=} 从数据库中返回一次性存储的班级课表。")
        return await apply_enhance(course_list, student.week, student.img)
    if student.username and student.password:
        try:
            async with jwxt(student.username, student.password) as zf:
                course_list = course_list_serializer(await zf.get_class_schedule())
                logger.success(
                    f"{student.username} | {student.week=} 获取指定学生的班级课表成功。",
                )
                return await apply_enhance(course_list, student.week, student.img)
        except LoginError as e:
            return ReturnDto(success=False, message=str(e))

    else:
        logger.error(
            f"参数错误，请同时携带或同时不携带学号和密码参数: {student.username=} | {student.password=}",
        )
        return ReturnDto(
            success=False,
            message="参数错误，请同时携带或同时不携带学号和密码参数。",
        )


@api_router.post("/schedule/student")
async def post_schedule_student(student: ScheduleQueryDto) -> ReturnDto:
    if student.username is None or student.password is None:
        logger.error("查询学生课表需要同时提供学号和密码参数。")
        return ReturnDto(
            success=False,
            message="查询学生课表需要同时提供学号和密码参数。",
        )

    try:
        async with jwxt(student.username, student.password) as zf:
            course_list = course_list_serializer(await zf.get_student_schedule())
            logger.success(f"{student.username} | 获取学生个人课表成功。")
            return await apply_enhance(course_list, student.week, student.img)
    except LoginError as e:
        return ReturnDto(success=False, message=str(e))


@api_router.get("/schedule/img/{name}")
async def get_schedule_img(name: str) -> FileResponse:
    """
    从 temp 工作目录中读取指定图片并返回。如果图片不存在则报 404。

    Returns:
        FileResponse: 图片。

    Raises:
        HTTPException: 404 - 查找的图片不存在。
    """
    image_file = TEMP_DIR / name
    logger.debug(f"尝试获取 {image_file!s}")
    if image_file.exists():
        return FileResponse(path=str(image_file), media_type="image/png")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Name wrong or too late.",
    )
