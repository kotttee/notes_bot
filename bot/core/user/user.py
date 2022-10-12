from bot.core.database import Database


class User:
    def __init__(self, properties: dict, user_id: int) -> None:
        if properties is None:
            self.user_id: int = user_id
            self.language: str | None = None
        else:
            self.language: str = properties['language']

    async def commit(self) -> None:
        await Database.save_user(self.__dict__)
