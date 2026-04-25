import time

from fastmcp.server.middleware import CallNext, MiddlewareContext
from fastmcp.server.middleware.middleware import Middleware
from fastmcp.tools import ToolResult
from mcp import types as mt

from . import config
from .logger import logger


class LoggingMiddleware(Middleware):
    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        tool_name = context.message.name
        args = context.message.arguments

        start_time = time.time()
        logger.debug(f"MCP → 调用工具: {tool_name}")
        if config.get("log", "log_mcp_request_details", False):
            logger.debug(f"调用参数 - {args=}")

        try:
            result = await call_next(context)
            elapsed = time.time() - start_time
            logger.info(f"MCP ← 工具 {tool_name} 完成, 耗时: {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(
                f"MCP ✗ 工具 {tool_name} 失败, 耗时: {elapsed:.3f}s, 错误: {e}",
            )
            raise
