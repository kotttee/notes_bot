from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from fluentogram import TranslatorHub

from bot.core.configuration import Configuration
from bot.core.user import User


# several middlewares doing the same function are made in order to mitigate changes in their work in the future

class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        hub: TranslatorHub = data.get('_translator_hub')
        user: User = data.get('_user')
        if user.language is None:
            if user.language is None:
                data['_i18n'] = hub.get_translator_by_locale(
                    event.from_user.language_code
                    if event.from_user.language_code in Configuration.available_languages() else 'en')

                user.language = event.from_user.language_code \
                    if event.from_user.language_code in Configuration.available_languages() else 'en'
        else:
            data['_i18n'] = hub.get_translator_by_locale(
                user.language if user.language in Configuration.available_languages() else 'en')
        return await handler(event, data)


class TranslatorRunnerCallbackMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        hub: TranslatorHub = data.get('_translator_hub')
        user: User = data.get('_user')
        if user.language is None:
            if user.language is None:
                data['_i18n'] = hub.get_translator_by_locale(
                    event.from_user.language_code
                    if event.from_user.language_code in Configuration.available_languages() else 'en')

                user.language = event.from_user.language_code \
                    if event.from_user.language_code in Configuration.available_languages() else 'en'
        else:
            data['_i18n'] = hub.get_translator_by_locale(
                user.language if user.language in Configuration.available_languages() else 'en')
        return await handler(event, data)
