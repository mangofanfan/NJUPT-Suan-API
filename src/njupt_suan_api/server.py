import asyncio
import time
import traceback
from contextlib import asynccontextmanager, suppress
from pathlib import Path
from typing import AsyncGenerator, Callable

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastmcp.utilities.lifespan import combine_lifespans
from watchfiles import awatch

from njupt_suan_api.api.baselib import (
    LogRecord,
    config,
    log_buffer,
    log_record_serialize,
    logger,
)
from njupt_suan_api.router import ASSETS_DIR, __version__, admin_router, api_router, mcp_app, webui_router
from njupt_suan_api.router.enhance import ReturnDto, create_db_and_tables

DATA_DIR = Path.cwd() / "data"

description = """
🚀 NJUPT Suan API 的 API 文档在此。你也可以直接在此处测试 API。

**NJUPT Suan API** 是一个为南京邮电大学（NJUPT）开发的项目。

**项目** -
[GitHub](https://github.com/mangofanfan/njupt-suan-api) |
[Mango Gitea](https://gitea.mangofanfan.cn/SuanDev/njupt-suan-api) |
[文档](https://suan.mangofanfan.cn)

**文档** - [SwaggerUI](/docs) | [Redoc](/redoc) | [openapi.json](/openapi.json)

### 如果您是访客

部分 **admin** 分组的端点需要身份验证才能调用，它们一般会被标记。

你可以在这里查看所有端点的详细信息，如果你需要进行针对 Suan API 的开发的话，这一定会对你有所帮助。

### 如果您是管理员

文档功能作为 FastAPI 的特色功能默认开启。

如果你需要，在 Suan API 的设置中可以选择关闭文档功能。
"""

config.sync_load_json()


async def toml_watcher() -> None:
    """配置文件监听器"""
    async for change in awatch(DATA_DIR / "config.json"):
        logger.info(f"配置文件更新，重新加载 | {change=}")
        await config.load_json()


@asynccontextmanager
async def life_span(_: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("初始化 SQLite 数据库中...")
    create_db_and_tables()
    logger.info("启动配置文件监听任务...")
    watcher_task = asyncio.create_task(toml_watcher(), name="toml_watcher")
    logger.success("🌟 NJUPT API Suan 已经启动。")
    try:
        yield
    finally:
        logger.info("🌙 NJUPT API Suan 正在关闭。")
        watcher_task.cancel()
        logger.info("配置文件监听任务已结束。")


# 文档功能是对 FastAPI app 实例进行配置的
enable_docs = config.get("system", "docs", True)
logger.debug(f"FastAPI 文档功能状态 - {enable_docs=}")

app = FastAPI(
    title="njupt-suan-api",
    lifespan=combine_lifespans(life_span, mcp_app.lifespan),
    description=description,
    docs_url="/docs" if enable_docs else None,
    redoc_url="/redoc" if enable_docs else None,
    openapi_url="/openapi.json" if enable_docs else None,
    version=__version__,
    license_info={"name": "MIT", "identifier": "MIT"},
)


@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> None:
    # 忽略对路径 /mcp 好 /mcp/ 的日志记录
    if request.url.path == "/mcp" or request.url.path == "/mcp/":
        return await call_next(request)

    # 如有需要，忽略对路径 /assets/ 的日志记录
    if not config.get("log", "log_assets_request", False) and request.url.path.startswith("/assets/"):
        return await call_next(request)

    # 请求开始时间
    start_time = time.time()

    # 获取请求信息
    client_host = request.client.host if request.client else "unknown"
    method = request.method
    path = request.url.path

    # 记录请求开始
    logger.debug(f"访问 [{client_host}] {method} {path}")
    if config.get("log", "log_api_request_details", False):
        logger.debug(f" - {request.headers=}")
        logger.debug(f" - {request.path_params=}")
        logger.debug(f" - {request.query_params=}")
        logger.debug(f" - request.body={await request.body()}")

    # 处理请求
    try:
        response = await call_next(request)

        # 计算耗时
        process_time = (time.time() - start_time) * 1000

        # 记录响应
        if response.status_code < 400:
            logger.info(
                f"成功 [{client_host}] {method} {path} | Status: {response.status_code} | Time: {process_time:.2f}ms",
            )
            if config.get("log", "log_api_request_details", False):
                logger.debug(f" - {response}")
        else:
            logger.warning(
                f"警告 [{client_host}] {method} {path} | Status: {response.status_code} | Time: {process_time:.2f}ms",
            )

        # 可以添加响应头（可选）
        response.headers["X-Process-Time"] = str(process_time)
        return response

    except Exception as exc:
        process_time = (time.time() - start_time) * 1000
        logger.error(
            f"错误 [{client_host}] {method} {path} | Error: {exc} | Time: {process_time:.2f}ms",
        )
        raise


@app.websocket("/ws/logs")
async def ws_logs(websocket: WebSocket) -> None:
    """向 WebUI 传递 Suan API 日志"""  # noqa: DOC501
    await websocket.accept()
    logger.debug("日志 websocket 建立连接，日志将被推送到 WebUI。")
    last_sent_id = 0

    try:
        while True:
            new_logs = [log for log in log_buffer if log.id >= last_sent_id]
            if new_logs:
                try:
                    await asyncio.wait_for(
                        websocket.send_json(
                            {
                                "logs": [log_record_serialize(log) for log in new_logs],  # 新日志
                                "latest_id": LogRecord.log_counter,
                            },
                        ),
                        timeout=2.0,
                    )
                except asyncio.TimeoutError:
                    logger.debug("日志 websocket 发送超时，已自动退出。")
                    break
                last_sent_id = LogRecord.log_counter

            try:
                await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                raise
    except WebSocketDisconnect:
        logger.debug("日志 websocket 断开连接。")
    except asyncio.CancelledError:
        logger.debug("日志 websocket 任务取消。")
    except Exception as exc:
        logger.error(f"向 WebUI 传递日志时遇到异常 : {exc}")
    finally:
        with suppress(Exception):
            await websocket.close()


@app.get("/version")
async def get_version() -> ReturnDto:
    ver = {"version": __version__}
    return ReturnDto(success=True, result=ver)


app.include_router(api_router)
app.include_router(admin_router)
app.include_router(webui_router)
app.mount("/mcp", mcp_app)
app.mount(
    "/assets",
    StaticFiles(directory=ASSETS_DIR),
    name="assets",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["mcp-session-id"],  # 关键：必须显式暴露此 Header
)


@app.exception_handler(Exception)
def general_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    # 记录错误堆栈
    logger.error(
        f"未捕获的异常！这可能表示某些路由、端点已经不可用！\n{exc!s}\n{traceback.format_exc()}",
    )

    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None,  # 生产环境不要暴露详细错误信息
        },
    )
