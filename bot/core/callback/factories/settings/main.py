from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from .translations import *
from bot.core.configuration import Configuration


class SettingsCallbackFactory(CallbackData, prefix="main_callback"):
    action: str
    value: str

    @staticmethod
    async def get_settings_keyboard_fab(lang_code: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for k, v in globals()[lang_code]['settings'].items():
            builder.button(
                text=v,
                callback_data=SettingsCallbackFactory(action="get_settings", value=k)
            )
        builder.adjust(2)
        return builder.as_markup()

    @staticmethod
    async def get_settings_language_keyboard_fab() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for lang in Configuration.available_languages():
            builder.button(
                text=lang,
                callback_data=SettingsCallbackFactory(action="change_language", value=lang)
            )
        builder.button(
            text='⛔',
            callback_data=SettingsCallbackFactory(action='get_settings', value='cancel')
        )
        return builder.as_markup()

    @staticmethod
    async def get_settings_loop_notes_keyboard_fab(lang_code: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for k, v in globals()[lang_code]['settings_loop_notes'].items():
            builder.button(
                text=v,
                callback_data=SettingsCallbackFactory(action="loop_notes", value=k)
            )
        builder.button(
            text='⛔',
            callback_data=SettingsCallbackFactory(action='get_settings', value='cancel')
        )
        builder.adjust()
        return builder.as_markup()

    @staticmethod
    async def get_support_answer_fab(chat_id: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
                text='ответить',
                callback_data=SettingsCallbackFactory(action="answer_support", value=str(chat_id))
            )
        return builder.as_markup()
