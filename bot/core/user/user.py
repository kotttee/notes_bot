import datetime

from bot.core.database import Database
from bot.core.notes import Note, EmptyNote


class User:
    def __init__(self, properties: dict, user_id: int, note: Note | EmptyNote, looped_users_skips: dict, database: Database) -> None:
        self.__database = database
        self.note = note
        self.user_id: int = user_id
        if properties is None:
            self.language: str | None = None
            self.loop_notes = False
        else:
            self.loop_notes = properties['loop_notes']
            self.language: str = properties['language']
            self.active: bool = properties['active']
            if user_id not in looped_users_skips.keys():
                looped_users_skips[user_id] = []
            self.looped_notes_skips = looped_users_skips[user_id]

    @property
    def data(self) -> dict:
        return {'user_id': self.user_id, 'language': self.language, 'active': self.active, 'loop_notes': self.loop_notes}

    async def update_note(self, text: str) -> None:
        self.note.showed = []
        self.note.date = datetime.datetime.now().timestamp()
        self.note.text = text
        self.note.language = self.language
        await self.note.commit()

    async def commit(self) -> None:
        await self.__database.save_user(self.data)
