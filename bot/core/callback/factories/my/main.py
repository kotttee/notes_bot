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
        for k, v in globals()[lang_code]['my_menu'].items():
            builder.button(text=v)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    async def get_cancel_keyboard_fab() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(
            text='⛔.',)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    async def rate_note_factory() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(
            text='😺.',)
        builder.button(
            text='✏.',)
        builder.button(
            text='⛔.', )
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    async def generate_answer_for_comment(lang_code: str, note_id: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
                text=globals()[lang_code]['answer_comment']['answer'],
                callback_data=MyCallbackFactory(action="answer_comment", value=str(note_id))
            )
        return builder.as_markup()
