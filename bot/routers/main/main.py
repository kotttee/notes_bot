from aiogram import Router, Bot
from aiogram.types import Message, BotCommandScopeChat, ChatMemberUpdated
from aiogram.filters import Command, IS_NOT_MEMBER, IS_MEMBER, ChatMemberUpdatedFilter
from fluentogram import TranslatorRunner
from bot.core.callback import MainCallbackFactory as MainCbFac
from bot.core.user import User
from bot.core.commands import MainCommands
from aiogram import F
from aiogram.fsm.context import FSMContext

main_router = Router()


# main
@main_router.message(Command(commands=["start"]))
async def process_start_command(message: Message, _i18n: TranslatorRunner, _user: User, bot: Bot):
    _user.active = True
    await _user.commit()
    await message.answer(_i18n.main.greeting())
    await bot.set_my_commands(await MainCommands.get_default_commands(_user.language),
                              BotCommandScopeChat(chat_id=_user.user_id),
                              _user.language)
    await message.answer(_i18n.main.menu(), reply_markup= await MainCbFac.get_menu_keyboard_fab(_user.language))


@main_router.message(Command(commands=["menu"]))
async def process_menu_command(message: Message, _i18n: TranslatorRunner, _user: User):
    await message.answer(_i18n.main.menu(), reply_markup= await MainCbFac.get_menu_keyboard_fab(_user.language))


@main_router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def handle_block(event: ChatMemberUpdated, _user: User):
    _user.active = False
    await _user.commit()


@main_router.message(F.text == '⛔.')
async def get_settings(message: Message, state: FSMContext, _i18n: TranslatorRunner, _user: User):
    await state.clear()
    await message.answer(_i18n.main.menu(), reply_markup= await MainCbFac.get_menu_keyboard_fab(_user.language))


@main_router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def handle_unblock(event: ChatMemberUpdated, _user: User):
    _user.active = True
    await _user.commit()


