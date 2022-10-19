from bot.core.database import Database
import re
from .note import Note


forbidden_words = ['блять', 'сука']


class NotesManager:

    @staticmethod
    async def get_note_of_user(user_id: int, database: Database) -> Note:
        note = await database.



    @staticmethod
    async def check_note(text: str) -> tuple:
        """returns 'status' and 'description', if everything is ok with the note, then the status will be True,
        otherwise False and 'description' will contain the reason for the problem"""
        for word in forbidden_words:
            if re.search(word, text):
                return False, 'contains_forbidden_words'

        return True, 'ok'
