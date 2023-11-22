import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.bot.schemas.dispatcher_data import DispatcherData
from src.database.database import Database

logger = logging.getLogger(__name__)


class ArchiveUser(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: DispatcherData,
    ) -> Any:
        db: Database = data['db']
        if not await db.user.check_user(event.from_user.id):
            await db.user.new(user_id=event.from_user.id,
                              user_name=event.from_user.username,
                              chat_id=event.chat.id
                              )
            await db.session.commit()
            logger.info(f"New user: {event.from_user.id} was added to database")

        return await handler(event, data)
