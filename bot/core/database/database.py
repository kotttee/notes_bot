from motor.motor_asyncio import AsyncIOMotorClient

from .requests import *


class Database:
    def __init__(self, client: AsyncIOMotorClient) -> None:
        self.database = client.notes_bot

    async def get_user(self, user_id: int) -> dict | None:
        return await get_user_request(user_id, self.database.users)

    async def save_user(self, user: dict) -> None:
        """the dictionary should contain information about the instance of the User class"""
        await update_user_request(user, self.database.users)

    async def get_note(self, note_id: int) -> None | dict:
        """the story_id should be the same as a chat_id"""
        return await get_note_request(note_id, self.database.notes)

    async def save_note(self, data: dict) -> None:
        """the story_id should be the same as a chat_id"""
        await update_note_request(data, self.database.notes)

    async def get_notes_filtered(self, note_filter: dict, loop_notes: bool, skip: list):
        while True:
            note = await get_note_filtered_request(note_filter, skip, self.database.notes)
            if note == "BREAK":
                break
            if not note:
                if loop_notes:
                    skip.clear()
                    continue
                break
            else:
                yield note, skip
