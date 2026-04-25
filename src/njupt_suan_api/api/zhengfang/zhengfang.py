from ddddocr import DdddOcr
from playwright.async_api import Browser, BrowserContext, Page, Playwright

from ..baselib import PlayContextManager, logger
from .createcourse import create_course_schedule
from .exc import LoginError
from .sso import SSO
from .types import Course


class ZhengFang(PlayContextManager):
    def __init__(
        self,
        playwright: Playwright = None,
        browser: Browser = None,
        context: BrowserContext = None,
        page: Page = None,
    ) -> None:
        super().__init__(playwright, browser, context, page)

    @classmethod
    async def init_from_sso(cls, sso: SSO) -> "ZhengFang":
        await sso.goto_zf()
        logger.info("从 SSO 进入正方教务系统。")
        return cls(sso.playwright, sso.browser, sso.context, sso.page)

    async def login(self, username: str, password: str) -> bool:
        """
        使用用户名和密码实现教务系统登录。

        Returns:
            bool，表明登录是否成功。

        Raises:
            LoginError: 登录失败，包含提示信息
        """
        await self.page.goto("http://jwxt.njupt.edu.cn")

        # 填充用户名和密码
        await self.page.fill("input#txtUserName", username)
        await self.page.fill("input#TextBox2", password)

        # 处理验证码
        captcha_img = self.page.locator("img#icode")
        captcha_bytes = await captcha_img.screenshot()
        ocr = DdddOcr(show_ad=False)
        captcha_code = str(ocr.classification(captcha_bytes))
        logger.debug(f"识别到的验证码为: {captcha_code}")
        await self.page.fill("input#txtSecretCode", captcha_code)

        async with self.page.expect_event("dialog", timeout=3000) as dialog_info:
            await self.page.click("input#Button1")
        dialog = await dialog_info.value
        if dialog.message == "请到信息维护中完善个人联系方式":
            await dialog.accept()
            logger.info(f"{username} | 登录正方教务系统成功。")
            self.isLogin = True
            return True
        if "验证码" in dialog.message:
            await dialog.accept()
            logger.warning(f"{username} | 验证码错误，自动重试...")
            return await self.login(username, password)
        await dialog.accept()
        logger.error(f"{username} | 登录失败，教务系统提示信息为: {dialog.message}")
        raise LoginError(dialog.message)

    async def get_class_schedule(self) -> list[Course]:
        await self.page.locator("a.top_link:has-text('公用信息')").click()
        await self.page.locator("a:has-text('班级课表查询')").click()
        sub_frame = self.page.frame_locator("iframe[name='zhuti']")
        logger.debug("获取班级课表。")
        return create_course_schedule(
            f"<table>{await sub_frame.locator('table#Table6').inner_html()}</table>",
        )

    async def get_student_schedule(self) -> list[Course]:
        await self.page.locator("a.top_link:has-text('信息查询')").click()
        await self.page.locator("a:has-text('学生个人课表')").click()
        sub_frame = self.page.frame_locator("iframe[name='zhuti']")
        logger.debug("获取个人课表。")
        return create_course_schedule(
            f"<table>{await sub_frame.locator('table#Table1').inner_html()}</table>",
        )
