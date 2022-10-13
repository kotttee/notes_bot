from bot.core.database import Database


class User:
    def __init__(self, properties: dict, user_id: int, database: Database) -> None:
        self.__database = database
        if properties is None:
            self.user_id: int = user_id
            self.language: str | None = None
        else:
            self.language: str = properties['language']

    async def commit(self) -> None:
        await self.__database.save_user(self.__dict__)
