from typing import Literal

import uuid6
import zstd
from nats.js import JetStreamContext
from ormsgpack import ormsgpack

from src.bot.utils.schemas.models import SerializedMessage
from src.database.database import Database


async def broadcast_task(jetstream: JetStreamContext, db: Database, send_data: SerializedMessage,
                         target: Literal['channel', 'user']):
    match target:
        case 'channel':
            sequence = await db.channel.get_channels_id(send_data.user_id)
        case 'user':
            sequence = await db.user.get_all()
    for object in sequence:
        await jetstream.publish(
            subject=f'service_notify.{target}_message',
            payload=zstd.compress(
                ormsgpack.packb(
                    {
                        'chat_id': send_data.chat_id,
                        'send_data': send_data
                    }
                )
            ),
            headers={
                'Nats-Msg-Id': uuid6.uuid8().hex,
            }
        )
