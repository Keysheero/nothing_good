from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.bot.schemas.dispatcher_data import DispatcherData
from src.database.database import Database


class DatabaseMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: DispatcherData,
    ) -> Any:
        async with data['pool']() as session:
            data['db'] = Database(session)
            return await handler(event, data)