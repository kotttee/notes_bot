from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluentogram import TranslatorRunner

from bot.core.callback import MyCallbackFactory as MyCbFac
from bot.core.database import Database
from bot.core.fsm import WriteNote
from bot.core.notes import NotesManager
from bot.core.user import User

my_menu_router = Router()


@my_menu_router.message(F.text == '📒.')
async def process_my_menu_command(message: Message, _i18n: TranslatorRunner, _user: User):
    if _user.note.valid:
        await message.answer(_i18n.main.my.menu_with_note(),
                             reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))
        await message.answer(_user.note.text)
    else:
        await message.answer(_i18n.main.my.menu_without_note(),
                             reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))


@my_menu_router.message(F.text == '📝.')
async def process_write_note_command(message: Message, _i18n: TranslatorRunner, _user: User, state: FSMContext):
    await message.answer(_i18n.main.my.write_note(),
                         reply_markup=await MyCbFac.get_cancel_keyboard_fab())
    await state.set_state(WriteNote.write_note)


@my_menu_router.message(WriteNote.write_note)
async def process_write_note_message_command(message: Message, _i18n: TranslatorRunner, _user: User, _db: Database,
                                             state: FSMContext):
    status, description = await NotesManager.check_note(message.text)
    if not status:
        await message.answer(eval(f'_i18n.main.my.check_error.{description}()'),
                             reply_markup=await MyCbFac.get_cancel_keyboard_fab())
        return
    else:
        await _user.update_note(message.text)
        await state.clear()
        await message.answer(_i18n.main.my.menu_with_note(),
                             reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))
        await message.answer(message.text)


@my_menu_router.message(F.text == '📖.')
async def process_show_note(message: Message, _i18n: TranslatorRunner, _user: User, _db: Database):
    note = await NotesManager.get_note(_user, _db)
    if note:
        await message.answer(_i18n.main.my.watch_notes(), reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))
        await message.answer(note.text, reply_markup=await MyCbFac.rate_note_factory())
    else:
        await message.answer(_i18n.main.my.no_notes(), reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))


@my_menu_router.message(F.text == '😾.')
async def process_show_note_next(message: Message, _i18n: TranslatorRunner, _user: User, _db: Database):
    note = await NotesManager.get_note(_user, _db)
    if note:
        await message.answer(note.text, reply_markup=await MyCbFac.rate_note_factory())
    else:
        await message.answer(_i18n.main.my.no_notes(), reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))
