from configparser import ConfigParser
import ast

parser = ConfigParser()
parser.read('bot.ini')


class Configuration:

    @staticmethod
    def database_connection() -> str:
        return parser.get('database', 'connection')

    @staticmethod
    def bot_token() -> str:
        return parser.get('bot', 'token')

    @staticmethod
    def available_languages() -> list:
        return ast.literal_eval(parser.get('languages', 'available'))

    @staticmethod
    def support_chat_id() -> int:
        return int(parser.get('bot', 'support_chat_id'))
