import asyncio
from aiogram import Bot, Dispatcher
from bot.core.configuration import Configuration
from bot.core.multilanguage import build_translator_hub, TranslatorRunnerMiddleware, TranslatorRunnerCallbackMiddleware
from bot.core.user import IncludeUserMiddleware, IncludeUserCallbackMiddleware, IncludeUserMyChatMemberMiddleware

from bot.routers import main_router, settings_router, my_menu_router


async def main():

    bot = Bot(await Configuration.bot_token(), parse_mode='html')
    dp = Dispatcher()

    # ROUTERS
    dp.include_router(main_router)
    dp.include_router(my_menu_router)
    dp.include_router(settings_router)

    # MIDDLEWARES
    # message
    dp.message.middleware(IncludeUserMiddleware())
    dp.message.middleware(TranslatorRunnerMiddleware())
    # callback
    dp.callback_query.middleware(IncludeUserCallbackMiddleware())
    dp.callback_query.middleware(TranslatorRunnerCallbackMiddleware())
    # my_chat_member
    dp.my_chat_member.middleware(IncludeUserMyChatMemberMiddleware())
    # OTHER
    queue = asyncio.Queue()
    translator_hub = await build_translator_hub(await Configuration.available_languages())

    # START
    await dp.start_polling(bot, _translator_hub=translator_hub, _run=queue.put)


asyncio.run(main())
