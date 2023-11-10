from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from nats.js import JetStreamContext

from src.bot.keyboards.keyboard import Keyboard
from src.bot.middlewares.db_middleware import DatabaseMiddleware
from src.bot.middlewares.user_middleware import ArchiveUser
from src.bot.states.states_groups import FSMPosts
from src.bot.utils.utils import serialize_message
from src.database.database import Database
from src.services.nats.broadcast import  broadcast_task

router: Router = Router()

router.message.outer_middleware(DatabaseMiddleware())
router.message.middleware(ArchiveUser())
router.callback_query.outer_middleware(DatabaseMiddleware())
router.callback_query.middleware(ArchiveUser())


@router.message(F.text == 'Посты')
async def start_post_handler(message: Message, state: FSMContext, keyboard: Keyboard):
    await message.answer("Вы выбрали раздел посты, отправьте боту пост и он разошлет куда надо",
                         reply_markup=keyboard.create_inline_keyboard(
                             width=1, cancel='Отмена'
                         ))
    await state.set_state(FSMPosts.making_post)


@router.message(StateFilter(FSMPosts.making_post))
async def making_post_handler(message: Message, state: FSMContext, jetstream: JetStreamContext, db: Database):
    send_data = serialize_message(message)
    await broadcast_task(jetstream=jetstream, db=db, send_data=send_data, target='channel')
    await state.clear()
    await message.answer("Ахуенно")


