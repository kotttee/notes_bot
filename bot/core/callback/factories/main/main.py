from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from .translations import *


class MainCallbackFactory(CallbackData, prefix="main_callback"):
    action: str
    value: str

    @staticmethod
    async def get_menu_keyboard_fab(lang_code: str) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        for k, v in globals()[lang_code]['menu'].items():
            builder.button(text=v)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    async def get_cancel_keyboard_fab() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(
            text='⛔.', )
        return builder.as_markup(resize_keyboard=True)
