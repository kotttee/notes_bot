from motor.motor_asyncio import AsyncIOMotorClient
from bot.core.configuration import Configuration


client = AsyncIOMotorClient(Configuration.database_connection(), connect=True)
database = client.diaries_bot


async def get_users_collection():
    return database.users


async def get_stories_collection():
    return database.stories
