from contextlib import suppress
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from fluentogram import TranslatorRunner, TranslatorHub
from bot.core.fsm import ContactSupport
from bot.core.callback import SettingsCallbackFactory as SettingsCbFac
from bot.core.callback import MainCallbackFactory as MainCbFac
from bot.core.configuration import Configuration
from bot.core.user import User

settings_router = Router()


@settings_router.message(Command(commands=["settings"]))
@settings_router.message(F.text == '⚙.')
async def process_settings_command(message: Message, _i18n: TranslatorRunner, _user: User, bot: Bot):
    await message.answer(_i18n.main.settings(),
                         reply_markup=await SettingsCbFac.get_settings_keyboard_fab(_user.language))

    with suppress(TelegramBadRequest):
        await bot.delete_message(message.chat.id, message.message_id)


@settings_router.callback_query(SettingsCbFac.filter(F.action == "get_settings"))
async def get_settings(callback: CallbackQuery, callback_data: SettingsCbFac, _i18n: TranslatorRunner,
                       _user: User, bot: Bot, state: FSMContext):
    match callback_data.value:
        case 'language':
            await callback.message.answer(_i18n.main.settings.language(),
                                          reply_markup=await SettingsCbFac.get_settings_language_keyboard_fab())
        case 'loop_notes':
            await callback.message.answer(_i18n.main.settings.loop_notes(),
                                          reply_markup=await SettingsCbFac.get_settings_loop_notes_keyboard_fab(
                                              _user.language))
        case 'support':
            await state.set_state(ContactSupport.send_contact_message)
            await callback.message.answer(_i18n.main.settings.contact_support(),
                                          reply_markup=await MainCbFac.get_cancel_keyboard_fab())
        case 'cancel':
            pass
    with suppress(TelegramBadRequest):
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.answer()


@settings_router.callback_query(SettingsCbFac.filter(F.action == "change_language"))
async def change_language(callback: CallbackQuery, callback_data: SettingsCbFac, _translator_hub: TranslatorHub,
                          _user: User, bot: Bot):
    if callback_data.value not in Configuration.available_languages():
        await callback.answer(
            text='sorry this language is not available right now, maybe we are having problems with the translation',
            show_alert=True)
    else:
        _user.language = callback_data.value
        await _user.commit()
    _i18n = _translator_hub.get_translator_by_locale(_user.language)
    await callback.message.answer(_i18n.main.menu(), reply_markup=await MainCbFac.get_menu_keyboard_fab(_user.language))
    with suppress(TelegramBadRequest):
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)


@settings_router.callback_query(MainCbFac.filter(F.action == "loop_notes"))
async def change_loop_notes(callback: CallbackQuery, callback_data: MainCbFac, _i18n: TranslatorRunner,
                            _user: User, bot: Bot):
    _user.loop_notes = True if callback_data.value == 'true' else False
    await _user.commit()
    await callback.message.answer(_i18n.main.menu(), reply_markup=await MainCbFac.get_menu_keyboard_fab(_user.language))
    with suppress(TelegramBadRequest):
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)


@settings_router.message(ContactSupport.send_contact_message)
async def process_write_note_message_command(message: Message, _i18n: TranslatorRunner, _user: User,
                                             state: FSMContext, bot: Bot):
    await bot.send_message(Configuration.support_chat_id(),
                           "новое обращение в поддержку:\n" + message.text + '\nuser_id - ' + str(message.from_user.id),
                           reply_markup=await SettingsCbFac.get_support_answer_fab(message.chat.id))
    await state.clear()
    await message.answer(_i18n.main.success() + "\n" + _i18n.main.menu(),
                         reply_markup=await MainCbFac.get_menu_keyboard_fab(_user.language))


@settings_router.callback_query(MainCbFac.filter(F.action == "answer_support"))
async def answer_support(callback: CallbackQuery, callback_data: MainCbFac, _i18n: TranslatorRunner,
                         _user: User, state: FSMContext):
    await state.set_state(ContactSupport.answer_from_support)
    await state.set_data({'answer_to_chat': callback_data.value})
    await callback.answer('напиши пожалуйста ответ', show_alert=True)


@settings_router.message(ContactSupport.answer_from_support)
async def process_write_note_message_command(message: Message, _i18n: TranslatorRunner, _user: User,
                                             state: FSMContext, bot: Bot):
    state_data: dict = await state.get_data()
    await bot.send_message(state_data['answer_to_chat'], 'answer from support:\n' + message.text)
    await state.clear()
