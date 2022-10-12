from bot.core.database import Database
from .user import User


class UserManager:

    @staticmethod
    async def get_user(user_id: int) -> User:
        return User(await Database.get_user(user_id), user_id)

    @staticmethod
    async def save_user(user: User) -> None:
        await Database.save_user(user.__dict__)


