from bot.core.database import Database
from .user import User
from bot.core.notes import NotesManager

class UserManager:

    @staticmethod
    async def get_user(user_id: int, database: Database) -> User:
        return User(await database.get_user(user_id), user_id,
                    await NotesManager.get_note_of_user(user_id, database),
                    database)

    @staticmethod
    async def save_user(user: User, database: Database) -> None:
        await database.save_user(user.__dict__)
