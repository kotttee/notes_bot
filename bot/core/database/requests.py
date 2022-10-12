from . import sessions
from .sessions import get_users_collection


async def get_user_request(user_id: int) -> dict | None:
    collection = await get_users_collection()
    user = await collection.find_one(dict(user_id=user_id))
    return user


async def update_user_request(user: dict) -> None:
    collection = await get_users_collection()
    old_user = await collection.find_one(dict(user_id=user['user_id']))
    if old_user:
        await collection.replace_one(dict(_id=old_user['_id']), user)
    else:
        await collection.insert_one(user)