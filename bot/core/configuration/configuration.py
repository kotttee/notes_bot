from configparser import ConfigParser
import ast

parser = ConfigParser()
parser.read('bot.ini')


class Configuration:

    @staticmethod
    def database_connection() -> str:
        return parser.get('database', 'connection')

    @staticmethod
    async def bot_token() -> str:
        return parser.get('bot', 'token')

    @staticmethod
    async def available_languages() -> list:
        return ast.literal_eval(parser.get('languages', 'available'))
