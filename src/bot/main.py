import asyncio
import logging
import sys

import nats
from aiogram import Bot, Dispatcher
from nats.aio.client import Client
from nats.js import JetStreamContext
from redis.asyncio import Redis

from faststream.nats import NatsBroker
from faststream import FastStream

from src.bot.keyboards.keyboard import Keyboard
from src.database.database import get_async_sessionmaker
from src.bot.dispatcher import get_dispatcher, get_redis_storage
from src.config import conf
from src.bot.schemas.dispatcher_data import DispatcherData
from src.services.nats.worker import user_nats_polling, channel_nats_polling


async def main() -> None:
    logging.basicConfig(
        handlers=[
            logging.FileHandler('debug.log', encoding='utf-8', ),
            logging.StreamHandler(sys.stdout)
        ],
        level='DEBUG',
        force=True,
        format="%(levelname)-8s [%(asctime)s] :: %(name)s : %(message)s"
    )
    logger = logging.getLogger(__name__)

    storage = get_redis_storage(
        redis=Redis(
            db=conf.redis.db,
            host=conf.redis.host,
            port=conf.redis.port,
        )
    )

    bot: Bot = Bot(token=conf.bot.BOT_TOKEN)
    dp: Dispatcher = get_dispatcher(storage=storage)
    nats_client: Client = await nats.connect(
        servers=[
            conf.nats_server
        ],
    )
    jetstream: JetStreamContext = nats_client.jetstream()
    logger.info('Bot Launching')
    try:
        await jetstream.add_stream(
            name='service_notify',
            subjects=['service_notify.*'],
            retention='interest',
            storage='file'
        )
        await bot.delete_webhook(drop_pending_updates=True)
        await asyncio.gather(
            dp.start_polling(bot, **DispatcherData(pool=get_async_sessionmaker(),
                                                   keyboard=Keyboard()), jetstream=jetstream),
            user_nats_polling(bot=bot, jetstream=jetstream),
            channel_nats_polling(bot=bot, jetstream=jetstream)
        )
    finally:
        await storage.close()
        await bot.session.close()
        await nats_client.drain()


if __name__ == '__main__':
    asyncio.run(main())
