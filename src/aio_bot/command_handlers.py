from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram import F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import BaseModel
import logging


from src.api_client import JsonPlaceholderClient, GoogleSheetsExporter
from src.repositories.user_repository import UserRepository


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
            text="💾 Сохранить пользователей в БД",
            callback_data="get_users"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🗑️ Удалить пользователей",
            callback_data="delete_users"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📊 Сохранить в Google Sheets",
            callback_data="save_to_gsheets"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="ℹ️ О боте",
            callback_data="about"
        )
    )

    await message.answer(
        text,
        reply_markup=builder.as_markup(),
                         )

async def handle_callbacks(
        callback: types.CallbackQuery,
        api_client: JsonPlaceholderClient,
        api_google: GoogleSheetsExporter,
        user_repo: UserRepository
):
    """Обработчик нажатий на кнопки"""
    if callback.data == "get_users":
        try:
            users = await api_client.get_users()

            result = await user_repo.save_users(users)

            # Формируем ответ
            response = "\n".join(f"{u.name} - {u.email}" for u in users[:5])  # Берём первых 5 для примера
            await callback.message.edit_text(
                f"Сoхраненно {result} пользователей. \n "
                f"Первые 5 из сохраненных пользователей:\n{response}",
                reply_markup=callback.message.reply_markup)

        except Exception as e:
            await callback.message.edit_text(f"Ошибка: {str(e)}")
    elif callback.data == "save_to_gsheets":
        text = ("✅ Данные успешно экспортированы в Google Sheets \n"
                "https://docs.google.com/spreadsheets/d/1DvXeVBw0TLg8Gm8ZZEheSKoIOTLbJyXDTQd6wsyvx0s/edit?usp=sharing")
        try:
            await callback.answer("⏳ Сохраняем в Google Sheets...")
            users = await user_repo.get_all_users()
            is_ok_google = await api_google.export_users(users, "1DvXeVBw0TLg8Gm8ZZEheSKoIOTLbJyXDTQd6wsyvx0s")
            if not is_ok_google:
                text = "❌ Ошибка при экспорте в Google Sheets"
            await callback.message.edit_text(
                text,
                reply_markup=callback.message.reply_markup
            )
        except Exception as e:
            await callback.answer("❌ Ошибка при экспорте")
            logging.error(f"Google Sheets error: {e}")
    elif callback.data == "delete_users":
        await callback.message.edit_text(
            "реализация CRUD операций не была прописана в задании\n"
            "для реализации свяжитесь с разработчиком: \n"
            "Разработчик Писарев Николай  @Nikolay_Pisarev\n",
            reply_markup=callback.message.reply_markup
        )
    elif callback.data == "about":
        await callback.message.edit_text(
            "Это тестовый бот для работы с API\n"
            "Использует JSON Placeholder\n"
            "Разработчик Писарев Николай  @Nikolay_Pisarev\n"
            "Исходный код https://github.com/Pisarev82/test_task.git",
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
    dp.callback_query.register(handle_callbacks, F.data.in_(
        ["get_users", "delete_users", "save_to_gsheets", "about"]
        ))
    dp.message.register(get_users, Command("users"))
    dp.message.register(echo_text, F.text)