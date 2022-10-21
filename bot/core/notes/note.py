import datetime

from bot.core.database import Database


class Note:
    def __init__(self, text: str, note_id: int, date: float, language : str, showed: list, database: Database) -> None:
        self.__database: Database = database
        self.note_id: int = note_id
        self.text: str = text
        self.date: float = date
        self.language: str = language
        self.showed: list = showed

    @property
    def valid(self) -> bool:
        return self.date + 86400 > datetime.datetime.now().timestamp()

    @property
    def data(self) -> dict:
        return {'note_id': self.note_id, 'language': self.language, 'showed': self.showed,
                'date': self.date, 'text': self.text}

    async def commit(self) -> None:
        await self.__database.save_note(self.data)


class EmptyNote:
    def __init__(self, note_id: int, database: Database) -> None:
        self.__database: Database = database
        self.note_id: int = note_id
        self.text: str = ''
        self.date: float = 0.1
        self.language: str = ''
        self.showed: list = []

    @property
    def valid(self) -> bool:
        return False

    @property
    def data(self) -> dict:
        return {'note_id': self.note_id, 'language': self.language, 'showed': self.showed,
                'date': self.date, 'text': self.text}

    async def commit(self) -> None:
        await self.__database.save_note(self.data)
