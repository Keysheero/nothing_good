from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import BaseModel


class Channel(BaseModel):
    __tablename__ = 'channels'

    channel_id: Mapped[int] = mapped_column(String(length=32), primary_key=True)

    user: Mapped["User"] = relationship(back_populates='channel', uselist=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    def __repr__(self) -> str:
        return f'Channel:{self.channel_id}'
