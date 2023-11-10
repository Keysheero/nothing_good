import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from aiogram.types import Message
from loguru import logger
from nats.js import JetStreamContext
from ormsgpack import ormsgpack
import zstd

from src.bot.utils.schemas.models import SerializedMessage


async def channel_nats_polling(
        bot: Bot, jetstream: JetStreamContext
):
    logger.info('channel_nats_polling was started')

    channel_subscribe: jetstream.PushSubscription = await jetstream.subscribe(
        subject='service_notify.channel_message',
        stream='service_notify',
        durable='get_channel_message',
        manual_ack=True
    )
    async for message in channel_subscribe.messages:
        try:
            data = ormsgpack.unpackb(zstd.decompress(message.data))
            chat_id = data['chat_id']
            send_data: SerializedMessage = data['send_data']
            if send_data.photo is not None:
                await bot.send_photo(chat_id=chat_id,
                                     photo=send_data.photo,
                                     caption=send_data.caption
                                     )
            else:
                await bot.send_message(chat_id=chat_id,
                                       text=send_data.text)
                await message.ack()

        except TimeoutError:
            pass

        except TelegramRetryAfter as ex:
            logger.warning(f'Limit exceeded, continue in: {ex.retry_after}')
            await asyncio.sleep(float(ex.retry_after))
            continue

        except TelegramForbiddenError:
            logger.info('User blocked Bot')
            await message.ack()
            continue

        except BaseException as ex:
            logger.error(f'Unexpected error: {ex}')
            continue
    logger.info('channel_nats_polling was ended')

async def user_nats_polling(
        bot: Bot, jetstream: JetStreamContext
):
    logger.info('user_nats_polling was started')

    user_subscribe: jetstream.PushSubscription = await jetstream.subscribe(
        subject='service_notify.user_message',
        stream='service_notify',
        durable='get_user_message',
        manual_ack=True
    )
    async for message in user_subscribe.messages:
        try:
            data = ormsgpack.unpackb(zstd.decompress(message.data))
            chat_id = data['chat_id']
            send_data = data['send_data']

            await bot.send_message(chat_id=chat_id,
                                   text=send_data)
            await message.ack()

        except TimeoutError:
            pass

        except TelegramRetryAfter as ex:
            logger.warning(f'Limit exceeded, continue in: {ex.retry_after}')
            await asyncio.sleep(float(ex.retry_after))
            continue

        except TelegramForbiddenError:
            logger.info('User blocked Bot')
            await message.ack()
            continue

        except BaseException as ex:
            logger.error(f'Unexpected error: {ex}')
            continue

    logger.info('user_nats_polling was ended')
