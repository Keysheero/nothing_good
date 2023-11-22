import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError, TelegramBadRequest
from nats.js import JetStreamContext
from ormsgpack import ormsgpack
import zstd

logger = logging.getLogger(__name__)


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
            send_data = data['send_data']
            if send_data['photo'] is not None:
                await bot.send_photo(chat_id=chat_id,
                                     photo=send_data['photo'],
                                     caption=send_data['caption']
                                     )
                await message.ack()
                logger.info('photo was successfully processed')

            else:
                await bot.send_message(chat_id=chat_id,
                                       text=send_data['text'])
                await message.ack()
                logger.info('channel_message was successfully processed')

        except TimeoutError:
            pass

        except TelegramRetryAfter as ex:
            logger.warning(f'Limit exceeded, continue in: {ex.retry_after}')
            await asyncio.sleep(float(ex.retry_after))
            continue

        except TelegramForbiddenError:
            logger.warning('User blocked Bot')
            await message.ack()
            continue

        except TelegramBadRequest:
            logger.warning(f'chat_id: {chat_id} has wrong channel_name')
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
                                   text=send_data['text'])
            await message.ack()
            logger.info('user broadcast was successfully proceeded')

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
