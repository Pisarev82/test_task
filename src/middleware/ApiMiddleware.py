from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any
from aiogram.types import Message
from src.api_client import JsonPlaceholderClient, GoogleSheetsExporter
import aiohttp


class ApiMiddleware(BaseMiddleware):
    def __init__(self, api_google: GoogleSheetsExporter):
        self.api_google = api_google

    async def __call__(
        self,
        handler: Callable[[Message, dict], Awaitable[Any]],
        event: Message,
        data: dict
    ) -> Any:
        async with aiohttp.ClientSession() as session:
            data["api_client"] = JsonPlaceholderClient(session)
            data["api_google"] = self.api_google
            return await handler(event, data)
