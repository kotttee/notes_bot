from motor.motor_asyncio import AsyncIOMotorCollection


async def get_user_request(user_id: int, users_collection: AsyncIOMotorCollection) -> dict | None:
    user = await users_collection.find_one(dict(user_id=user_id))
    return user


async def update_user_request(user: dict, users_collection: AsyncIOMotorCollection) -> None:
    old_user = await users_collection.find_one(dict(user_id=user['user_id']))
    if old_user:
        await users_collection.replace_one(dict(_id=old_user['_id']), user)
    else:
        await users_collection.insert_one(user)