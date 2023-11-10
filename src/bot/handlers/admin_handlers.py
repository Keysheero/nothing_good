from aiogram import Router, F
from aiogram.types import Message
from nats.js import JetStreamContext

from src.bot.middlewares.admin_middleware import CheckAdmin
from src.bot.middlewares.db_middleware import DatabaseMiddleware
from src.database.database import Database
from src.services.nats.broadcast import broadcast_task

router: Router = Router()

router.message.outer_middleware(CheckAdmin())
router.callback_query.outer_middleware(CheckAdmin())
router.message.middleware(DatabaseMiddleware())
router.callback_query.middleware(DatabaseMiddleware())


@router.message(F.text[:9] == 'broadcast')
async def broadcast_handler(message: Message, db: Database, jetstream: JetStreamContext):
    send_data = message.text[9:]
    await broadcast_task(jetstream, db, send_data)
