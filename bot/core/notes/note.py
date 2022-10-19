import datetime

from bot.core.database import Database


class Note:
    def __init__(self, text: str, note_id: int, date: float, database: Database) -> None:
        self.__database: Database = database
        self.note_id: int = note_id
        self.text: str = text
        self.date: float = date

    @property
    async def is_valid(self) -> bool:
        return self.date + 86400 < datetime.datetime.now().timestamp()

    async def commit(self) -> None:
        await self.__database.save_note(self.note_id, self.text)
