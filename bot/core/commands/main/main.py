from aiogram.types import BotCommand
from .translations import *
from bot.core.configuration import Configuration


class MainCommands:

    @staticmethod
    async def get_default_commands(lang_code: str) -> list[BotCommand]:
        bot_commands = []
        for k, v in eval(lang_code)['default'].items():
            bot_commands.append(BotCommand(command=k, description=v))
        return bot_commands

