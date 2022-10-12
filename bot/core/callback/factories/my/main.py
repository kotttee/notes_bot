from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from .translations import *
from bot.core.configuration import Configuration


class MyCallbackFactory(CallbackData, prefix="main_callback"):
    action: str
    value: str

    @staticmethod
    async def get_my_menu_keyboard_fab(lang_code: str) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        for k, v in eval(lang_code)['my_menu'].items():
            builder.button(text=v)
        return builder.as_markup(resize_keyboard=True)
