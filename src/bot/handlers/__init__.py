from .basic_handlers import router as basic_router
from src.bot.handlers.user_handlers.channels_handlers import router as user_router
from src.bot.handlers.user_handlers.post_handlers import router as post_router
from .admin_handlers import router as admin_router

routers = (basic_router, user_router, admin_router, post_router)