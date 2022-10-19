from aiogram.fsm.state import StatesGroup, State


class WriteNote(StatesGroup):
    write_note = State()
