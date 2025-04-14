import logging

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from aiohttp import web

from config import BOT_TOKEN, local_run
from aio_bot.command_handlers import register_handlers
from middleware import ConfigMiddleware, ApiMiddleware

logging.basicConfig(level=logging.INFO)


# Инициализация бота, диспетчера и обработчиков
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.update.middleware(ConfigMiddleware(local_run))
dp.update.middleware(ApiMiddleware())
register_handlers(dp)

# Запуск для сервера на вебхуках
async def main_webhook():
    from config import WEBHOOK_URL, WEB_SERVER_HOST, WEB_SERVER_PORT, WEBHOOK_SECRET, WEBHOOK_PATH

    try:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            secret_token=WEBHOOK_SECRET,
            drop_pending_updates=True
        )
        logging.info(f"Webhook успешно установлен на {WEBHOOK_URL}")
    except Exception as e:
        logging.error(f"Ошибка установки webhook: {e}")
        raise

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    await site.start()

    logging.warning(f"Сервер запущен на {WEB_SERVER_HOST}:{WEB_SERVER_PORT}")
    await asyncio.Event().wait()

# Запуск для тестов на лонг поллинге
async def main_polling():
    # Удаляем вебхук для работы в режиме поллинга
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    if local_run:
        logging.info("Запуск в режиме polling (локально)")
        asyncio.run(main_polling())
    else:
        logging.warning("Запуск в режиме webhook (докер)")
        asyncio.run(main_webhook())
