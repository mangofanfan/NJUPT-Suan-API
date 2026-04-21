from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)


class PlayContextManager:
    def __init__(
        self,
        playwright: Playwright = None,
        browser: Browser = None,
        context: BrowserContext = None,
        page: Page = None,
    ) -> None:
        self.playwright = playwright
        self.browser = browser
        self.context = context
        self.page = page

        self.isLogin = False

    async def start(self) -> None:
        """手动启动"""
        self.playwright = await async_playwright().start()  # 不是 __enter__
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-proxy-server",
            ],
        )
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def __aenter__(self) -> "PlayContextManager":
        await self.start()
        return self

    async def close(self) -> None:
        """手动关闭"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()  # 不是 __exit__

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        await self.close()
