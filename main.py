from pathlib import Path
from secrets import token_urlsafe

from njupt_api.baselib import config, logger
from router import __version__

DATA_DIR = Path.cwd() / "data"
TEMP_DIR = Path.cwd() / "temp"


if __name__ == "__main__":
    try:
        with open(file=Path.cwd() / "njupt_api" / "art.txt", mode="r", encoding="utf-8") as f:
            print(f.read().format(__version__))  # noqa:T201
    except FileNotFoundError:
        pass

    import uvicorn

    logger.success("Ciallo~(∠·ω< )⌒★")

    # 创建需要的工作目录
    if DATA_DIR.exists() and DATA_DIR.is_dir():
        logger.debug(f"工作目录 {DATA_DIR=!s} 已存在。")
    else:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        logger.debug(f"工作目录 {DATA_DIR=!s} 已创建。")

    if TEMP_DIR.exists() and TEMP_DIR.is_dir():
        logger.debug(f"工作目录 {TEMP_DIR=!s} 已存在。")
        # 清空 temp 工作目录中的已有文件
        c = 0
        for item in TEMP_DIR.iterdir():
            item.unlink()
            c += 1
        logger.debug(f"清理了 temp 工作目录中的 {c} 个已有文件。")
    else:
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        logger.debug(f"工作目录 {TEMP_DIR=!s} 已创建。")

    # 如果没有 toml 配置文件就创建
    try:
        config.sync_load_json()
    except FileNotFoundError:
        config.init_config()
        config.sync_create_json()

    lines = [
        "",
        "🌐 WebUI 管理面板将运行在 /webui 端点下，登录需要令牌。",
        "",
        "============================================================",
        "🔐 管理后端令牌",
        "============================================================",
        "",
    ]
    try:
        with open(file=DATA_DIR / "token.txt", mode="r", encoding="utf-8") as f:
            token = f.readline().strip()
        lines.insert(-2, f"🔐 使用已经存在的管理后端令牌 | {token}")
    except FileNotFoundError:
        token = token_urlsafe(32)
        with open(file=DATA_DIR / "token.txt", mode="w", encoding="utf-8") as f:
            f.write(token)
        lines.insert(-2, f"🔐 新的管理后端令牌已生成 | {token}")
    lines.insert(-2, "🔐 你需要此令牌以登录管理员面板并可视化地配置 NJUPT Suan API。")
    logger.info("\n".join(lines))

    logger.info("🥭 准备 uvicorn run ...")
    host = config.get("system", "host", "0.0.0.0")
    port = config.get("system", "port", 8000)
    reload = config.get("system", "reload", True)
    logger.debug(f"启动参数 - {host=} | {port=} | {reload=}")
    logger.debug("这些参数无法自动热重载。如果你修改了他们，请 Ctrl + C 关闭并重新启动 Suan API。")
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=["njupt_api", "router"],
        access_log=False,
        log_level="critical",
        timeout_graceful_shutdown=2,
    )
    logger.debug("退出时未清理 temp 工作目录，将在 Suan API 下次启动时清理。")
    logger.info("🥭 uvicorn run 已结束。")
