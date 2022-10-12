from bot.core.database import Database


class StoryManager:

    def __init__(self, database: Database) -> None:
        self.database = database