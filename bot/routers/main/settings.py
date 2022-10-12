from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery, BotCommandScopeChat
from aiogram.filters import Command
from fluentogram import TranslatorRunner, TranslatorHub
from bot.core.callback import MainCallbackFactory as MainCbFac
from bot.core.user import User
from bot.core.configuration import Configuration
from bot.core.commands import MainCommands
from aiogram import F
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

settings_router = Router()


@settings_router.message(Command(commands=["settings"]))
@settings_router.message(F.text == '⚙.')
async def process_settings_command(message: Message, _i18n: TranslatorRunner, _user: User, bot: Bot):
    await message.answer(_i18n.main.settings(),
                         reply_markup=await MainCbFac.get_settings_keyboard_fab(_user.language))

    with suppress(TelegramBadRequest):
        await bot.delete_message(message.chat.id, message.message_id)


@settings_router.callback_query(MainCbFac.filter(F.action == "get_settings"))
async def get_settings(callback: CallbackQuery, callback_data: MainCbFac, _i18n: TranslatorRunner,
                       _user: User, bot: Bot):
    match callback_data.value:
        case 'language':
            await callback.message.answer(_i18n.main.settings.language(),
                                          reply_markup=await MainCbFac.get_settings_language_keyboard_fab())
    match callback_data.value:
        case 'cancel':
            pass
    with suppress(TelegramBadRequest):
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.answer()


@settings_router.callback_query(MainCbFac.filter(F.action == "change_language"))
async def change_language(callback: CallbackQuery, callback_data: MainCbFac, _translator_hub: TranslatorHub,
                          _user: User, bot: Bot):
    if callback_data.value not in await Configuration.available_languages():
        await callback.answer(
            text='sorry this language is not available right now, maybe we are having problems with the translation',
            show_alert=True)
    else:
        _user.language = callback_data.value
        await _user.commit()
    _i18n = _translator_hub.get_translator_by_locale(_user.language)
    await callback.message.answer(_i18n.main.menu(), reply_markup= await MainCbFac.get_menu_keyboard_fab(_user.language))
    with suppress(TelegramBadRequest):
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)

    await bot.set_my_commands(await MainCommands.get_default_commands(_user.language),
                              BotCommandScopeChat(chat_id=_user.user_id),
                              _user.language)

