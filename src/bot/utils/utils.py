from aiogram.types import Message

from src.bot.utils.schemas.models import SerializedMessage


def serialize_message(message: Message) -> SerializedMessage:
    return SerializedMessage(
        user_id=message.from_user.id,
        photo=message.photo[-1].file_id if message.photo else None,
        caption=message.caption if message.caption else None,
        chat_id=message.chat.id,
        text=message.text
    )
