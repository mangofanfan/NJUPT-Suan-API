from .__version__ import __version__ as __version__
from .admin_router import admin_router
from .api_router import api_router
from .mcp_router import mcp_app
from .webui_router import ASSETS_DIR, webui_router

__all__ = [
    admin_router,
    api_router,
    mcp_app,
    webui_router,
    __version__,
    ASSETS_DIR,
]
