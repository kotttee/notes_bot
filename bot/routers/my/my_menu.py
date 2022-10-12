from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery, BotCommandScopeChat, ChatMemberUpdated
from aiogram.filters import Command, IS_NOT_MEMBER, IS_MEMBER, ChatMemberUpdatedFilter
from fluentogram import TranslatorRunner
from bot.core.callback import MyCallbackFactory as MyCbFac
from bot.core.user import User
from bot.core.configuration import Configuration
from bot.core.commands import MainCommands
from aiogram import F
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

my_menu_router = Router()


@my_menu_router.message(F.text == '📒.')
async def process_start_command(message: Message, _i18n: TranslatorRunner, _user: User, bot: Bot):
    await message.answer(_i18n.main.my.menu(), reply_markup= await MyCbFac.get_my_menu_keyboard_fab(_user.language))

