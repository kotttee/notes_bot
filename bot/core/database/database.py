import datetime

from motor.motor_asyncio import AsyncIOMotorClient
from .requests import get_user_request, update_user_request, update_note_request


class Database:
    def __init__(self, client: AsyncIOMotorClient) -> None:
        self.database = client.notes_bot

    async def get_user(self, user_id: int) -> dict | None:
        return await get_user_request(user_id, self.database.users)

    async def save_user(self, user: dict) -> None:
        """the dictionary should contain information about the instance of the User class"""
        if "_User__database" in user.keys():
            user.pop("_User__database")
        await update_user_request(user, self.database.users)

    async def get_note(self, note_id: int) -> None:
        """the story_id should be the same as a chat_id"""
        await get_note_request(note_id, text, datetime.datetime.now().timestamp(), self.database.notes)

    async def save_note(self, note_id: int, text: str) -> None:
        """the story_id should be the same as a chat_id"""
        await update_note_request(note_id, text, datetime.datetime.now().timestamp(), self.database.notes)