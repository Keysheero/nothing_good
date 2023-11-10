from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.config import conf
from .repository.channel import ChannelRepository
from .repository.user import UserRepository

def get_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


def get_async_sessionmaker(engine: AsyncEngine = None) -> async_sessionmaker:
    return async_sessionmaker(engine or create_async_engine(url=conf.db.build_connection_str()),
                              class_=AsyncSession,
                              expire_on_commit=False)


class Database:

    user: UserRepository
    channel: ChannelRepository

    def __init__(
            self, session: AsyncSession, user: UserRepository = None, channel: ChannelRepository = None
    ):
        self.session = session
        self.user = user or UserRepository(session=session)
        self.channel = channel or ChannelRepository(session)
