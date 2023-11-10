from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String(length=32))

    channel: Mapped["Channel"] = relationship(back_populates='user', uselist=False)

    def __repr__(self) -> str:
        return f'User:{self.user_name}:{self.user_id}'
