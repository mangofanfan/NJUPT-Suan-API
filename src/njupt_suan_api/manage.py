import subprocess
from secrets import token_urlsafe

import typer
from rich.console import Console
from rich.panel import Panel

from njupt_suan_api.api.baselib import config
from njupt_suan_api.cli import (
    ALREADY_INIT_MESSAGE,
    DATA_DIR,
    INIT_STAGE_MESSAGE,
    NOT_INIT_MESSAGE,
    RUN_CHECK_MESSAGE,
    TEMP_DIR,
    TOKEN_CHECK_MESSAGE,
    WORKSPACE_DIR,
)
from njupt_suan_api.router import __version__

console = Console()
app = typer.Typer(
    name="NJUPT-Suan-API",
    help="NJUPT Suan API 部署与管理工具",
    rich_markup_mode="rich",
    no_args_is_help=True,
)


def version_callback(value: bool = False) -> None:
    if value:
        console.print(f"NJUPT Suan API [green]v.{__version__}[/green]")
        if __version__ == "dev":
            console.print("""
[bright_black]显示的版本为 dev ？这是因为你正在从源代码运行 cli 入口（manage.py）。[/bright_black]
[bright_black]从[green]已安装版本[/green]中运行 [green]suanapi --version[/green] 可以正确获取版本号。[/bright_black]""")
        raise typer.Exit


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="显示版本号并退出，没有其他命令会被执行。",
        callback=version_callback,
        is_eager=True,  # 优先处理，避免触发其他逻辑
    ),
) -> None:
    """
    CLI 入口回调，所有子命令执行前都会经过这里。
    可以在这里放全局初始化（如日志级别、环境检查）。
    """
    pass  # 没有 --version 时就正常放行，继续执行子命令


@app.command()
def init(force: bool = typer.Option(False, "--force", "-f", help="强制初始化，可能导致问题，不建议使用。")) -> None:
    """
    初始化 NJUPT Suan API [green]工作目录[/green]。（可能需要较长时间）

    会在当前目录或指定目录下创建新文件，并尝试安装 playwright chromium。
    视网络情况，安装过程可能（几乎必然）需要较长时间。
    如果已存在 data 和/或 temp 目录，初始化会失败。你也可以强制初始化，但可能导致先前的数据丢失。

    Raises:
        typer.Exit: 如果初始化失败，返回 1。
    """
    if (DATA_DIR.exists() or TEMP_DIR.exists()) and not force:
        console.print(Panel(ALREADY_INIT_MESSAGE, title="工作目录已存在"))
        console.print("[bright_black]如果你想要强制初始化，使用 [green]suanapi init -f[/green] 命令。[/bright_black]")
        raise typer.Exit(code=1)

    # 1 创建 data 和 temp 目录
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    console.print(INIT_STAGE_MESSAGE.format(stage=1, message="工作目录 data 和 temp 已创建。"))

    # 2 初始化配置文件
    try:
        config.sync_load_json()
    except FileNotFoundError:
        config.init_config()
        config.sync_create_json()
        console.print(INIT_STAGE_MESSAGE.format(stage=2, message="已初始化配置并创建配置文件。"))
    else:
        console.print(INIT_STAGE_MESSAGE.format(stage=2, message="配置文件已存在，跳过配置初始化。"))

    # 3 执行 uv run playwright install chromium
    console.print("[bright_black]即将安装 playwright 的 chromium，这可能是耗时最长的部分。[/bright_black]")
    cp3 = subprocess.run(["playwright", "install", "chromium"], cwd=WORKSPACE_DIR)
    if cp3.returncode != 0:
        console.print("[yellow]运行 playwright install chromuim 失败，双是什么原因呢？[/yellow]")
        raise typer.Exit(code=cp3.returncode)
    console.print(INIT_STAGE_MESSAGE.format(stage=3, message="已安装 playwright chromium。"))

    console.print("[green]初始化完成。接下来可以执行 suanapi run 来启动 NJUPT Suan API。[/green]")
    console.print(
        "[bright_black]初始化只需要执行一次即可，以后即使更新 NJUPT Suan API，也无再需重复执行。[/bright_black]"
    )


@app.command()
def token(reset: bool = typer.Option(False, "--reload", "-r", help="强制重新生成令牌，即使令牌已存在。")) -> None:
    """
    查看或重新生成[green]管理后端令牌[/green]。

    需要先运行过 init 初始化目录。

    Raises:
        typer.Exit: 如果未初始化，返回 1。
    """
    token_ = None
    # 首先检查数据目录是否存在
    if not DATA_DIR.exists():
        console.print(Panel(NOT_INIT_MESSAGE, title="数据目录不存在"))
        raise typer.Exit(code=1)

    # 确认存在后再判断是否需要重新生成令牌
    if not reset:
        try:
            with open(file=DATA_DIR / "token.txt", mode="r") as f:
                token_ = f.read()
        except FileNotFoundError:
            pass
    if not token_:
        console.print("[yellow]重新生成令牌...[/yellow]")
        token_ = token_urlsafe(32)
        with open(file=DATA_DIR / "token.txt", mode="w") as f:
            f.write(token_)

    panel = Panel(TOKEN_CHECK_MESSAGE.format(token=token_), title="WebUI 令牌")

    console.print(panel)


@app.command()
def run(
    host: str | None = typer.Option(None, "--host", help="监听主机名，默认 0.0.0.0。"),
    port: int | None = typer.Option(None, "--port", help="监听端口，默认 8000。"),
    reload: bool | None = typer.Option(None, "--reload", "-r", help="在检测到代码变化时自动重启，默认 False。"),
) -> None:
    """
    运行 NJUPT Suan API。

    可接收运行参数。若不提供，则尝试使用配置文件中的值，最后回退到默认值。

    Raises:
        typer.Exit: 如果未初始化，返回 1。
    """
    if host is None:
        host = config.get("system", "host", "0.0.0.0")
    if port is None:
        port = config.get("system", "port", 8000)
    if reload is None:
        reload = config.get("system", "reload", False)

    if not DATA_DIR.exists() or not TEMP_DIR.exists():
        console.print(Panel(NOT_INIT_MESSAGE, title="工作目录不存在"))
        raise typer.Exit(code=1)

    token(False)

    console.print(Panel(RUN_CHECK_MESSAGE.format(host=host, port=port, reload=reload), title="运行前检查"))

    import uvicorn

    uvicorn.run(
        "njupt_suan_api.server:app",
        host=host,
        port=port,
        reload=reload,
        access_log=False,
        log_level="critical",
        timeout_graceful_shutdown=2,
    )


if __name__ == "__main__":
    app()
