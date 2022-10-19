from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery, BotCommandScopeChat
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner, TranslatorHub
from bot.core.callback import MyCallbackFactory as MyCbFac
from bot.core.user import User
from bot.core.database import Database
from bot.core.fsm import WriteNote
from aiogram import F
from bot.core.notes import NotesManager
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

my_menu_router = Router()


@my_menu_router.message(F.text == '📒.')
async def process_my_menu_command(message: Message, _i18n: TranslatorRunner, _user: User, bot: Bot, state: FSMContext):
    await message.answer(_i18n.main.my.menu(),
                         reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))


@my_menu_router.message(F.text == '📝.')
async def process_write_note_command(message: Message, _i18n: TranslatorRunner, _user: User, bot: Bot, state: FSMContext):
    await message.answer(_i18n.main.my.write_note(),
                         reply_markup=await MyCbFac.get_cancel_keyboard_fab())
    await state.set_state(WriteNote.write_note)


@my_menu_router.message(WriteNote.write_note)
async def process_write_note_message_command(message: Message, _i18n: TranslatorRunner, _user: User, _db: Database, state: FSMContext):
    status, description = await NotesManager.check_note(message.text)
    if not status:
        await message.answer(eval(f'_i18n.main.my.check_error.{description}()'),
                             reply_markup=await MyCbFac.get_cancel_keyboard_fab())
        return
    else:
        await _db.save_note(message.chat.id, message.text)
        await state.clear()
        await message.answer(_i18n.main.my.write_note_done(),
                             reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))