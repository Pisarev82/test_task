from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any
from aiogram.types import Message
from src.api_client import JsonPlaceholderClient
import aiohttp


class ApiMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict], Awaitable[Any]],
        event: Message,
        data: dict
    ) -> Any:
        async with aiohttp.ClientSession() as session:
            data["api_client"] = JsonPlaceholderClient(session)
            return await handler(event, data)
