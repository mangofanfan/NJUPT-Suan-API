from njupt_api.baselib import PlayContextManager, logger

from .exc import LoginError


class SSO(PlayContextManager):
    def __init__(self) -> None:
        super().__init__()

    async def login(self, username: str, password: str) -> bool:
        """使用用户名和密码实现登录南邮统一身份验证。

        Parameters:
            username: 用户名，学号，一般为一位大写字母+八位数字
            password: 密码

        Returns:
            bool，表明判登录是否成功。

        Raises:
            LoginError: 登录失败，暂时不包含任何提示信息……
        """
        await self.page.goto("http://i.njupt.edu.cn/")

        await self.page.fill('input[name="username"]', username)
        await self.page.fill('input[type="password"]', password)
        await self.page.click('button[type="button"]')

        await self.page.wait_for_load_state("networkidle")
        if "user-login" in self.page.url:
            logger.error(f"{username} | 登录失败，请检查学号和密码是否正确。")
            raise LoginError("unknown")

        logger.info(f"{username} | 登录南邮统一身份认证成功。")
        self.isLogin = True
        return True

    async def goto_zf(self) -> None:
        sub_frame = self.page.frame_locator('iframe[name="iframe0"]')
        async with self.context.expect_event("page") as new_page_event:
            await sub_frame.locator('a[title="教务系统"]').click()
        self.page = await new_page_event.value
        return
