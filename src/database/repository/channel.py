from typing import Any

from sqlalchemy import select, Row, Sequence, Select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..models.base import BaseModel
from ..models.channel import Channel


class ChannelRepository(Repository[Channel]):

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Channel, session=session)

    async def new(self, channel_id, user_fk):
        await self.session.merge(
            self.type_model(channel_id=channel_id,
                            user_fk=user_fk)
        )

    async def delete(self, user_fk) -> None:
        statement = delete(self.type_model).where(self.type_model.user_fk == user_fk)
        await self.session.execute(statement)


    async def get_channels_id(self, user_fk: int) -> list[str]:
        statement: Select[tuple[Any]] = select(self.type_model.channel_id).where(self.type_model.user_fk == user_fk)
        result = await self.session.execute(statement)
        return [channel_id for (channel_id, ) in result.all()]

