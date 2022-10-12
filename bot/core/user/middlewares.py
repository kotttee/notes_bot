from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

from . import UserManager


class IncludeUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        data['_user'] = await UserManager.get_user(event.from_user.id)
        return await handler(event, data)


class IncludeUserCallbackMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[ChatMemberUpdated, Dict[str, Any]], Awaitable[Any]],
            event: ChatMemberUpdated,
            data: Dict[str, Any]
    ) -> Any:
        data['_user'] = await UserManager.get_user(event.from_user.id)
        return await handler(event, data)


class IncludeUserMyChatMemberMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        data['_user'] = await UserManager.get_user(event.from_user.id)
        return await handler(event, data)

