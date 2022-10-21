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


async def get_note_request(note_id: int, notes_collection: AsyncIOMotorCollection) -> dict | None:
    note = await notes_collection.find_one(dict(note_id=note_id))
    return note


async def update_note_request(data: dict, notes_collection: AsyncIOMotorCollection) -> None:
    old_note = await notes_collection.find_one(dict(note_id=data['note_id']))
    if old_note:
        await notes_collection.replace_one(dict(_id=old_note['_id']), data)
    else:
        await notes_collection.insert_one(data)


async def get_note_filtered_request(note_filter: dict, skip: list, notes_collection: AsyncIOMotorCollection) -> dict | None:
    async for note in notes_collection.find(note_filter):
        if note:
            if note['note_id'] in skip:
                continue
        return note
