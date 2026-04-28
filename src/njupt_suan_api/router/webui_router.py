from pathlib import Path

import aiofiles
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

STATIC_DIR = Path(__file__).parent.parent / "static"
WEBUI_INDEX = STATIC_DIR / "index.html"
SCHEDULE_INDEX = STATIC_DIR / "index-schedule.html"
ASSETS_DIR = STATIC_DIR / "assets"

webui_router = APIRouter(prefix="/webui", tags=["webui"])


@webui_router.get("/", response_class=HTMLResponse)
async def get_webui() -> HTMLResponse:
    async with aiofiles.open(file=WEBUI_INDEX, mode="r", encoding="utf-8") as f:
        return HTMLResponse(content=await f.read(), status_code=200)


@webui_router.get("/schedule", response_class=HTMLResponse)
async def get_webui_schedule() -> HTMLResponse:
    async with aiofiles.open(file=SCHEDULE_INDEX, mode="r", encoding="utf-8") as f:
        return HTMLResponse(content=await f.read(), status_code=200)
