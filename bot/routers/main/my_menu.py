from aiogram import F, Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fluentogram import TranslatorRunner
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
from bot.core.callback import MyCallbackFactory as MyCbFac
from bot.core.callback import MainCallbackFactory as MainCbFac
from bot.core.database import Database
from bot.core.fsm import WriteNote, ReadNotes
from bot.core.notes import NotesManager
from bot.core.user import User

my_menu_router = Router()


@my_menu_router.message(F.text == '📒.')
async def process_my_menu_command(message: Message, _i18n: TranslatorRunner, _user: User):
    if _user.note.valid:
        await message.answer(_i18n.main.my.menu_with_note(views=len(_user.note.showed)),
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
        await message.answer(_i18n.main.my.menu_with_note(views=0),
                             reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))
        await message.answer(message.text)


@my_menu_router.message(F.text == '📖.')
async def process_show_note(message: Message, _i18n: TranslatorRunner, _user: User, _db: Database, state: FSMContext):
    note = await NotesManager.get_note(_user, _db)
    if note:
        await state.set_data({'read_note_id': note.note_id})
        await message.answer(_i18n.main.my.watch_notes(),
                             reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))
        await message.answer(note.text, reply_markup=await MyCbFac.rate_note_factory())
    else:
        await message.answer(_i18n.main.my.no_notes(),
                             reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))


@my_menu_router.message(F.text == '✏.')
async def process_comment_note(message: Message, _i18n: TranslatorRunner, _user: User, _db: Database,
                               state: FSMContext):
    await state.set_state(ReadNotes.comment_note)
    await message.answer(_i18n.main.my.comment_note(), reply_markup=await MyCbFac.get_cancel_keyboard_fab())


@my_menu_router.message(F.text == '😺.')
async def process_show_note_next(message: Message, _i18n: TranslatorRunner, _user: User, _db: Database,
                                 state: FSMContext):
    note = await NotesManager.get_note(_user, _db)
    if note:
        await state.set_data({'read_note_id': note.note_id})
        await message.answer(note.text, reply_markup=await MyCbFac.rate_note_factory())
    else:
        await message.answer(_i18n.main.my.no_notes(),
                             reply_markup=await MyCbFac.get_my_menu_keyboard_fab(_user.language))


@my_menu_router.message(ReadNotes.comment_note)
async def process_comment_note_message_command(message: Message, _i18n: TranslatorRunner, _user: User, _db: Database,
                                               state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    if 'read_note_id' in state_data.keys():
        status, desc = await NotesManager.check_comment(message.text)
        if status:
            with suppress(TelegramBadRequest):
                await bot.send_message(state_data['read_note_id'],
                                       _i18n.main.my.someone_commented_note() + '\n' + message.text,
                                       reply_markup=await MyCbFac.generate_answer_for_comment(_user.language,
                                                                                              _user.user_id))
    await state.clear()
    await message.answer(_i18n.main.success())
    await process_show_note_next(message, _i18n, _user, _db, state)


@my_menu_router.callback_query(MyCbFac.filter(F.action == "answer_comment"))
async def answer_to_comment_callback(callback: CallbackQuery, callback_data: MyCbFac, _i18n: TranslatorRunner,
                                     _user: User, bot: Bot, state: FSMContext):
    await state.set_state(ReadNotes.answer_for_comment)
    await state.set_data({'answer_to_chat': callback_data.value})
    await bot.send_message(callback.message.chat.id, _i18n.main.my.answer_to_comment(),
                           reply_markup=await MyCbFac.get_cancel_keyboard_fab())
    with suppress(TelegramBadRequest):
        await bot.edit_message_text(callback.message.text, callback.message.chat.id, callback.message.message_id)
    await callback.answer()


@my_menu_router.message(ReadNotes.answer_for_comment)
async def process_reply_to_comment(message: Message, _i18n: TranslatorRunner, _user: User,
                                   state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    if 'answer_to_chat' in state_data.keys():
        status, desc = await NotesManager.check_comment(message.text)
        if status:
            with suppress(TelegramBadRequest):
                await bot.send_message(state_data['answer_to_chat'],
                                       _i18n.main.my.you_have_answer_to_comment() + '\n' + message.text, )
    await state.clear()
    await message.answer(_i18n.main.success() + '\n' + _i18n.main.menu(),
                         reply_markup=await MainCbFac.get_menu_keyboard_fab(_user.language))
