from contextlib import asynccontextmanager
from typing import AsyncGenerator

from ..baselib import config
from .exc import LoginError
from .sso import SSO
from .zhengfang import ZhengFang


@asynccontextmanager
async def jwxt(username: str, password: str) -> AsyncGenerator[ZhengFang, None]:
    """
    根据设置，选择 SSO 登录教务系统或直接登录教务系统。

    Args:
        username: 用户名，str
        password: 密码，str

    Yields:
        zf: ZhengFang

    Raises:
        LoginError: 登录失败，包含下层返回的提示信息。
    """
    try:
        if config.get("schedule", "jwxt_login_method", "sso"):
            sso = SSO()
            await sso.start()
            await sso.login(username, password)
            zf = await ZhengFang.init_from_sso(sso)
        else:
            zf = ZhengFang()
            await zf.start()
            await zf.login(username, password)
    except LoginError as e:
        raise e
    else:
        yield zf
        await zf.close()
        return
