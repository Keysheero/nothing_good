from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ChatAdministratorRights

from src.bot.handlers.basic_handlers import command_start_handler
from src.bot.keyboards.keyboard import Keyboard
from src.bot.middlewares.db_middleware import DatabaseMiddleware
from src.bot.middlewares.user_middleware import ArchiveUser
from src.bot.states.states_groups import FSMChannels
from src.database.database import Database

router: Router = Router()

router.message.outer_middleware(DatabaseMiddleware())
router.message.middleware(ArchiveUser())
router.callback_query.outer_middleware(DatabaseMiddleware())
router.callback_query.middleware(ArchiveUser())


@router.message(F.text == 'Каналы')
async def start_channels_handler(message: Message, keyboard: Keyboard):
    await message.answer('Вы выбрали раздел Каналы'
                         'Выберите что вы хотите сделать', reply_markup=keyboard.create_inline_keyboard(
        add_channels='Добавить канал',
        del_channels='Удалить канал',
        cancel='Отмена'
    ))


@router.callback_query(F.data == 'cancel')
async def cancel_handler(callback: CallbackQuery, state: FSMContext, keyboard: Keyboard):
    await callback.message.delete()
    await command_start_handler(callback.message, keyboard, state)


@router.callback_query(F.data == 'add_channels')
async def callback_add_channel_handler(callback: CallbackQuery, state: FSMContext, keyboard: Keyboard):
    await callback.message.delete()
    await callback.message.answer('Напишите сюда канал для добавления',
                                  reply_markup=keyboard.create_inline_keyboard(cancel='Отмена'))
    await state.set_state(FSMChannels.add_channel)


@router.message(StateFilter(FSMChannels.add_channel))
async def sfm_add_channel_handler(message: Message, db: Database, state: FSMContext):
    try:
        await db.channel.new(channel_id=str(message.text),
                             user_fk=message.from_user.id)
        await db.session.commit()
        await message.answer("Успешно добавлено")


    except Exception as e:
        print(e)
        await message.answer("Вы ввели неправильно айди канала")
    await state.clear()


@router.callback_query(F.data == 'del_channels')
async def del_channel_handler(callback: CallbackQuery, db: Database, state: FSMContext, keyboard: Keyboard):
    await callback.message.delete()
    channels: list[str] = await db.channel.get_channels_id(user_fk=callback.from_user.id)
    if not channels:
        await callback.message.answer('У вас нету добавленных каналов')
        await state.clear()
    await callback.message.answer('Выберите канал для удаления', reply_markup=keyboard.create_inline_keyboard(
        1, cancel='Отмена', *channels
    ))

    await state.set_state(FSMChannels.del_channel)


@router.callback_query(StateFilter(FSMChannels.del_channel))
async def fsm_callback_del_channel(callback: CallbackQuery, db: Database, state: FSMContext):
    await callback.message.delete()
    try:
        await db.channel.delete(callback.from_user.id)
        await db.session.commit()
        await state.clear()
        await callback.answer('Успешно!', show_alert=True)
    except:
        await callback.message.answer("Произошла ошибка при эксплотутации бота, попробуйте еще раз!")
