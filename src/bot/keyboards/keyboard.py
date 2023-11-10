from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class Keyboard:

    def create_inline_keyboard(self, width: int = 1, *args, **kwargs) -> InlineKeyboardMarkup:
        ikb: InlineKeyboardBuilder = InlineKeyboardBuilder()
        buttons: list[InlineKeyboardButton] = []
        for button in args:
            buttons.append(InlineKeyboardButton(text=button, callback_data=button))

        for callback_data, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))
        return ikb.row(*buttons, width=width).as_markup()

    def create_keyboard(self, width: int, *args, **kwargs) -> ReplyKeyboardMarkup:
        rkb: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = []
        for button in args:
            buttons.append(KeyboardButton(text=button))
        for text in kwargs.values():
            buttons.append(KeyboardButton(text=text))
        return rkb.row(width=width, *buttons).as_markup()
