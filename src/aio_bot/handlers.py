from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram import F
import logging
# from src.config import local_run


async def cmd_start(message: Message):
    logging.info(f"Пользователь {message.from_user.username} вызвал команду /start")
    text = "👋 Я эхобот на вебхуках!"
    # if local_run:
    #     text = "👋 Я эхобот на локальном компьютере (Лонг Полинг)!"
    await message.answer(text)


async def echo_text(message: Message):
    logging.info(f"Пользователь {message.from_user.username} отправил сообщение: {message.text}")
    await message.answer(f"🔁 Вы сказали: <i>{message.text}</i>", parse_mode=ParseMode.HTML)


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(echo_text, F.text)