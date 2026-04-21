from pathlib import Path
from typing import Annotated, Sequence

import aiofiles
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, delete, select

from njupt_api.baselib import config, logger
from njupt_api.zhengfang import LoginError, course_list_serializer, jwxt
from router.enhance.auth import verify_token
from router.enhance.lib import AliasDto, ReturnDto, TestDto, get_session
from router.enhance.model import Alias, Course


class ValidateTokenDto(BaseModel):
    token: str


admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.post("/validateToken")
async def validate_token(vtd: ValidateTokenDto) -> ReturnDto:
    """
    验证 Token 是否正确，以此判断是否允许登录 WebUI。
    验证时无需使用 HTTP Bearer，直接作为 body 传入即可。

    Returns:
        ReturnDto，以 success 字段表明是否有效。
    """
    async with aiofiles.open(file=Path.cwd() / "data/token.txt", mode="r") as f:
        if (await f.readline()).strip() == vtd.token:
            return ReturnDto(success=True)
        return ReturnDto(success=False)


@admin_router.post("/schedule/test", dependencies=[Depends(verify_token)])
async def post_schedule_test(test: TestDto, session: Annotated[Session, Depends(get_session)]) -> ReturnDto:
    try:
        async with jwxt(test.username, test.password) as zf:
            if test.scheduleType == "class":
                final_course_list = course_list_serializer(
                    await zf.get_class_schedule(),
                )
                session.exec(delete(Course))
                for course in final_course_list:
                    session.add(Course(**course))
                session.commit()

                logger.success(
                    f"{test.username} | 获取 {test.scheduleType} 课表成功，已保存到数据库。",
                )
                return ReturnDto(success=True, result=final_course_list)
            if test.scheduleType == "student":
                final_course_list = course_list_serializer(
                    await zf.get_student_schedule(),
                )
                logger.success(
                    f"{test.username} | 获取 {test.scheduleType} 课表成功。个人课表不保存。",
                )
                return ReturnDto(success=True, result=final_course_list)
            logger.error(
                f"{test.username} | scheduleType 参数错误。给定的 schedule={test.scheduleType}",
            )
            return ReturnDto(
                success=False,
                message="参数错误，请检查 scheduleType 参数。",
            )
    except LoginError as e:
        return ReturnDto(success=False, message=str(e))


@admin_router.get("/schedule/test", dependencies=[Depends(verify_token)])
async def get_schedule_test(session: Annotated[Session, Depends(get_session)]) -> ReturnDto:
    course_dtos: Sequence[Course] = session.exec(select(Course)).all()
    return ReturnDto(
        success=True,
        result=[course.model_dump() for course in course_dtos],
    )


@admin_router.post("/schedule/alias", dependencies=[Depends(verify_token)])
async def post_schedule_alias(alias: AliasDto, session: Annotated[Session, Depends(get_session)]) -> ReturnDto:
    for alia in session.exec(select(Alias)).all():
        if alias.originalName == alia.originalName:
            logger.error(
                f"课程 {alia.originalName} 已经在数据库中存在，不允许重复添加。",
            )
            return ReturnDto(
                success=False,
                message=f"课程 {alia.originalName} 已经在数据库中存在，不允许重复添加。",
            )

    session.add(Alias(originalName=alias.originalName, aliasName=alias.aliasName))
    session.commit()
    logger.success(f"已添加课程别名 | {alias.originalName} => {alias.aliasName}")
    return ReturnDto(success=True)


@admin_router.get("/schedule/alias", dependencies=[Depends(verify_token)])
async def get_schedule_alias(session: Annotated[Session, Depends(get_session)]) -> ReturnDto:
    aliases: Sequence[Alias] = session.exec(select(Alias)).all()
    return ReturnDto(success=True, result=[alias.model_dump() for alias in aliases])


@admin_router.post("/config", dependencies=[Depends(verify_token)])
async def post_config(data: dict) -> ReturnDto:
    data_ = data.get("data")
    logger.debug(f"接收到配置字典 - {data_}")
    config.from_dict(data_)
    await config.save_json()
    return ReturnDto(success=True, result=config.to_dict())


@admin_router.get("/config", dependencies=[Depends(verify_token)])
async def get_config() -> ReturnDto:
    return ReturnDto(success=True, result=config.to_dict())
