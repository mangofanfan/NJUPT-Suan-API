from pathlib import Path

import aiofiles
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

WEBUI_INDEX = Path.cwd() / "webui" / "dist" / "index.html"
SCHEDULE_INDEX = Path.cwd() / "webui" / "dist" / "index-schedule.html"

webui_router = APIRouter(prefix="/webui")


@webui_router.get("/", response_class=HTMLResponse)
async def get_webui() -> HTMLResponse:
    async with aiofiles.open(file=WEBUI_INDEX, mode="r", encoding="utf-8") as f:
        return HTMLResponse(content=await f.read(), status_code=200)


@webui_router.get("/schedule", response_class=HTMLResponse)
async def get_webui_schedule() -> HTMLResponse:
    async with aiofiles.open(file=SCHEDULE_INDEX, mode="r", encoding="utf-8") as f:
        return HTMLResponse(content=await f.read(), status_code=200)
