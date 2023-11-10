from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.bot.schemas.dispatcher_data import DispatcherData
from src.config import conf


class CheckAdmin(BaseMiddleware):
    """This middleware throw a Database class to handler"""

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: DispatcherData,
    ) -> Any:
        admin_ids = conf.admin_ids
        if str(event.from_user.id) in admin_ids:
            return await handler(event, data)
        else:
            print('THERE WAS SOMETHING BAD WITH MIDDLEWARE')
