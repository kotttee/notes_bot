from bot.core.database import Database
import re
from bot import core
from .note import Note, EmptyNote

forbidden_words = ['блять', 'сука']

class NotesManager:

    @staticmethod
    async def get_note_of_user(user_id: int, database: Database) -> Note | EmptyNote:
        note = await database.get_note(user_id)
        if note is None:
            return EmptyNote(user_id, database)
        else:
            return Note(note['text'], user_id, note['date'], note['language'], note['showed'], database)

    @staticmethod
    async def check_note(text: str) -> tuple:
        """returns 'status' and 'description', if everything is ok with the note, then the status will be True,
        otherwise False and 'description' will contain the reason for the problem"""
        for word in forbidden_words:
            if re.search(word, text):
                return False, 'contains_forbidden_words'

        return True, 'ok'

    @staticmethod
    async def get_note(user, database: Database) -> Note | None:
        note = None
        async for i in database.get_notes_filtered({'language': user.language}):
            # here will be more filters soon
            if user.user_id not in i['showed']:
                note = Note(i['text'], i['note_id'], i['date'], i['language'], i['showed'], database)
                note.showed.append(user.user_id)
                await note.commit()
            break
        return note
