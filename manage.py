from secrets import token_urlsafe

import typer
from rich.console import Console
from rich.panel import Panel

from cli import ALREADY_INIT_MESSAGE, DATA_DIR, NOT_INIT_MESSAGE, TEMP_DIR
from router import __version__

console = Console()
app = typer.Typer(
    name="NJUPT-Suan-API",
    help="NJUPT Suan API 部署与管理工具",
    rich_markup_mode="rich",
    no_args_is_help=True,
    options_metavar="[选项]",
    subcommand_metavar="[命令]",
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
def init() -> None:
    """
    初始化 NJUPT Suan API [green]工作目录[/green]。（可能需要较长时间）

    会在当前目录或指定目录下创建新文件，并尝试安装 playwright chromium，安装过程可能需要较长时间。
    """
    if DATA_DIR.exists() or TEMP_DIR.exists():
        console.print(Panel(ALREADY_INIT_MESSAGE, title="数据目录已存在"))
        console.print("[bright_black]如果你想要强制初始化，使用 [green]suanapi init -f[/green] 命令。[/bright_black]")
        return


@app.command()
def token(reset: bool = typer.Option(False, "--reload", "-r", help="强制重新生成令牌，即使令牌已存在。")) -> None:
    """
    查看或重新生成[green]管理后端令牌[/green]。

    需要先运行过 init 初始化目录。

    Args:
        reset: bool，默认为 False，即只查看，在不存在时重新生成。
    """
    token_ = None
    # 首先检查数据目录是否存在
    if not DATA_DIR.exists():
        console.print(Panel(NOT_INIT_MESSAGE, title="数据目录不存在"))
        return

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

    msg = f"""
🔐 [green]  令牌 - [/green]{token_}
🔐 [green]有效期 - [/green]无限
✅ WebUI 设计的令牌 cookie 有效期为一天，所以你每天都需要重新登录一次 WebUI，这并非令牌本身的有效期。
"""

    panel = Panel(msg, title="WebUI 令牌")

    console.print(panel)


@app.command()
def run() -> None:
    """
    运行 NJUPT Suan API。
    """
    pass


if __name__ == "__main__":
    app()
