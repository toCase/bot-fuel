from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

def keyboard_start() -> ReplyKeyboardMarkup:
    key_builder = ReplyKeyboardBuilder()
    key_builder.row(
        KeyboardButton(text="INFO"),
        width=1
    )
    return  key_builder.as_markup(resize_keyboard=True)