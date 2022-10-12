from . import requests
from .requests import get_user_request, update_user_request


class Database:

    @staticmethod
    async def get_user(user_id: int) -> dict | None:
        return await get_user_request(user_id)

    @staticmethod
    async def save_user(user: dict) -> None:
        await update_user_request(user)



