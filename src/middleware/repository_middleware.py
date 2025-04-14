from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any
from aiogram.types import TelegramObject
from src.repositories import UserRepository
from src.repositories import db

class RepositoryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        async with db.session_factory() as session:
            data["user_repo"] = UserRepository(session)
            return await handler(event, data)