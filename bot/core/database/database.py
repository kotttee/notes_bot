from motor.motor_asyncio import AsyncIOMotorClient
from .requests import get_user_request, update_user_request


class Database:
    def __init__(self, client: AsyncIOMotorClient) -> None:
        self.database = client.notes_bot

    async def get_user(self, user_id: int) -> dict | None:
        return await get_user_request(user_id, self.database.users)

    async def save_user(self, user: dict) -> None:
        """the dictionary should contain information about the instance of the User class"""
        await update_user_request(user, self.database.users)
