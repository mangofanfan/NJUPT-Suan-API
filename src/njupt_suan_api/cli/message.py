NOT_INIT_MESSAGE = """
❓ 当前目录或指定目录下[yellow]似乎还没有执行过初始化命令[/yellow]。
❓ 你也许需要先执行 [green]suanapi init[/green] 。
"""

ALREADY_INIT_MESSAGE = """
❕ 当前目录或指定目录下[yellow]似乎已经执行初始化命令过[/yellow]。
❕ 你也许需要先删除已经存在的 [blue]data[/blue] 和 [blue]temp[/blue] 目录。
"""

RUN_CHECK_MESSAGE = """
[bright_black]运行时的配置可能来自命令行参数、配置文件以及默认值，列在这里供你检查。[/bright_black]
      [cyan]主机名[/cyan] -   [cyan]host[/cyan] - {host}
        [cyan]端口[/cyan] -   [cyan]port[/cyan] - {port}
    [cyan]自动重启[/cyan] - [cyan]reload[/cyan] - {reload}
[bright_black]NJUPT Suan API 会很快启动。使用 [green]Ctrl + C[/green] 以退出。[/bright_black]
"""

TOKEN_CHECK_MESSAGE = """
🔐 [green]  令牌 - [/green]{token}
🔐 [green]有效期 - [/green]无限
✅ WebUI 设计的令牌 cookie 有效期为一天，所以你每天都需要重新登录一次 WebUI，这并非令牌本身的有效期。
"""

INIT_STAGE_MESSAGE = "[cyan]- {stage} / 3 -[/cyan] [bright_black]{message}[/bright_black]"
