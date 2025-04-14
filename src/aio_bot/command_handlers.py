from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram import F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import BaseModel
import logging


from src.api_client import JsonPlaceholderClient
from src.repositories.user_base_repository import UserRepository


class UserResponse(BaseModel):
    user_id: int
    full_name: str
    contact_email: str


async def cmd_start(message: Message, local_run: bool):
    logging.info(f"Пользователь {message.from_user.username} вызвал команду /start")
    text = "👋 Я эхобот на вебхуках!"
    if local_run:
        text = "👋 Я эхобот на локальном компьютере (Лонг Полинг)!"

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="📋 Получить пользователей",
            callback_data="get_users"
        ),
        types.InlineKeyboardButton(
            text="ℹ️ О боте",
            callback_data="about"
        )
    )

    await message.answer(
        text,
        reply_markup=builder.as_markup(),
                         )

async def handle_callbacks(callback: types.CallbackQuery, api_client: JsonPlaceholderClient):
    """Обработчик нажатий на кнопки"""
    if callback.data == "get_users":
        users = await api_client.get_users()
        response = "\n".join(f"{user.name} - {user.email}" for user in users[:3])
        await callback.message.edit_text(
            f"Последние пользователи:\n{response}",
            reply_markup=callback.message.reply_markup
        )
    elif callback.data == "about":
        await callback.message.edit_text(
            "Это тестовый бот для работы с API\n"
            "Использует JSON Placeholder",
            reply_markup=callback.message.reply_markup
        )
    await callback.answer()


async def get_users(
        message: types.Message,
        api_client: JsonPlaceholderClient,
        user_repo: UserRepository
):
    try:
        users = await api_client.get_users()

        result = await user_repo.save_users(users)

        # Формируем ответ
        response = "\n".join(f"{u.name} - {u.email}" for u in users[:5]) # Берём первых 5 для примера
        await message.answer(f"Сoхраненно {result} пользователей. \n Первые 5 из сохраненных пользователей:\n{response}")

    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

async def echo_text(message: Message):
    logging.info(f"Пользователь {message.from_user.username} отправил сообщение: {message.text}")
    await message.answer(f"🔁 Вы сказали: <i>{message.text}</i>", parse_mode=ParseMode.HTML)


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.callback_query.register(handle_callbacks, F.data.in_(["get_users", "about"]))
    dp.message.register(get_users, Command("users"))
    dp.message.register(echo_text, F.text)