from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from src.bot.keyboards.keyboard import Keyboard
from src.bot.middlewares.db_middleware import DatabaseMiddleware
from src.bot.middlewares.user_middleware import ArchiveUser
from src.database.database import Database

router: Router = Router()

router.message.outer_middleware(DatabaseMiddleware())
router.message.middleware(ArchiveUser())
router.callback_query.outer_middleware(DatabaseMiddleware())
router.callback_query.middleware(ArchiveUser())


@router.message(CommandStart())
async def command_start_handler(message: Message, keyboard: Keyboard, state: FSMContext):
    await message.answer('Приветсвую тебя в этом замечательном боте\n\n'
                         'Бот предназначен для рассылки различных сообщений\n\n'
                         'Выберите до 5 каналов, и рассылайте по ним сообщения',
                         reply_markup=keyboard.create_keyboard(channels='Каналы📬', posts='Посты📩', width=1))
    await state.clear()

# @router.message(Command=['/help'])
# async def command_help_handler(message: Message):
#     await message.answer('Вы можете добавить до 10 каналов, в которых может происходить рассылка'
#                          'При получение каких-либо ошибок во время эксплуатации бота используйте /start')


# @router.message(Command=['/channels'])




