import dataclasses

from pydantic import BaseModel


@dataclasses.dataclass
class SerializedMessage:
    user_id: str | int
    photo: str | None
    caption: str | None
    chat_id: str | int
    text: str
