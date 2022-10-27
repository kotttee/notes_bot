from aiogram.fsm.state import StatesGroup, State


class WriteNote(StatesGroup):
    write_note = State()


class ReadNotes(StatesGroup):
    comment_note = State()
    answer_for_comment = State()


class ContactSupport(StatesGroup):
    send_contact_message = State()
    answer_from_support = State()
