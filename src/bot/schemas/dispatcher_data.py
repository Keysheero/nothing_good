

from typing import TypedDict

from aiogram import Bot
from sqlalchemy.ext.asyncio import  async_sessionmaker

from src.bot.keyboards.keyboard import Keyboard
from src.database.database import Database


class DispatcherData(TypedDict):
    """Common transfer data."""

    pool: async_sessionmaker
    keyboard: Keyboard
    db: Database | None
    bot: Bot | None