from aiogram import BaseMiddleware
from typing import Callable, Dict, Awaitable, Any
from aiogram.types import Message


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, local_run: bool):
        self.local_run = local_run

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        # Добавляем local_run в data
        data["local_run"] = self.local_run

        return await handler(event, data)