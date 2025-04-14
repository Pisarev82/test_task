from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram import F, types
from pydantic import BaseModel
import logging
from src.api_client import JsonPlaceholderClient

class UserResponse(BaseModel):
    user_id: int
    full_name: str
    contact_email: str


async def cmd_start(message: Message, local_run: bool):
    logging.info(f"Пользователь {message.from_user.username} вызвал команду /start")
    text = "👋 Я эхобот на вебхуках!"
    if local_run:
        text = "👋 Я эхобот на локальном компьютере (Лонг Полинг)!"
    await message.answer(text)


async def get_users(
        message: types.Message,
        api_client: JsonPlaceholderClient
):
    try:
        users = await api_client.get_users()

        # Преобразуем в нашу схему ответа
        response_data = [
            UserResponse(
                user_id=user.id,
                full_name=user.name,
                contact_email=user.email
            ) for user in users
        ]

        # Форматируем ответ
        response_text = "\n".join(
            f"👤 {user.full_name} (ID: {user.user_id})\n"
            f"📧 {user.contact_email}\n"
            for user in response_data[:5]  # Выводим первые 5 пользователей
        )

        await message.answer(response_text)

    except Exception as e:
        logging.error(f"API error: {e}")
        await message.answer("⚠ Ошибка при получении данных")

async def echo_text(message: Message):
    logging.info(f"Пользователь {message.from_user.username} отправил сообщение: {message.text}")
    await message.answer(f"🔁 Вы сказали: <i>{message.text}</i>", parse_mode=ParseMode.HTML)


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(echo_text, F.text)