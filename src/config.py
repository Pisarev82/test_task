import asyncio
import logging
import os
import socket
import sys

from urllib.parse import urlparse
from contextlib import closing
from dotenv import load_dotenv


load_dotenv("../.env")

# Загружаем константы которые нужны в любом случае
BOT_TOKEN = os.getenv("BOT_TOKEN")


POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


# Определяем где запущена программа
local_run = False
hostname = os.environ.get('COMPUTERNAME', os.environ.get('HOSTNAME'))
# немножко хардкода... Здесь оправданно...
print(hostname, hostname == "NIC")
if hostname == "NIC":
    local_run = True
    # Загружаем константы для локального запуска
    # from config_local import *
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    # Загружаем константы для запуска в докере

    # WEB_SERVER_HOST определен ниже
    # WEB_SERVER_PORT определен ниже
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    # WEBHOOK_PATH определен ниже
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


    def get_webhook_path(webhook_url):
        try:
            parsed = urlparse(WEBHOOK_URL)
            logging.info(f"Полученный URL: {parsed}")
            if not parsed.path or parsed.path == '/':
                return '/webhook'  # значение по умолчанию
            return parsed.path
        except Exception as e:
            logging.error(f"Ошибка парсинга WEBHOOK_URL: {e}")
            return '/webhook'  # fallback значение

    WEBHOOK_PATH = get_webhook_path(WEBHOOK_URL)


    def check_port_available(host: str, port: int) -> bool:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            return sock.connect_ex((host, port)) != 0

    def set_WEB_SERVER_HOST_and_PORT():
        WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
        WEB_SERVER_PORT = os.getenv("WEB_SERVER_PORT")
        is_port_available = check_port_available(WEB_SERVER_HOST, int(WEB_SERVER_PORT))
        logging.info(f"Порт {WEB_SERVER_PORT} доступен {is_port_available}")
        if not is_port_available:
            logging.error(f"Порт {WEB_SERVER_PORT} не доступен. Завершение работы программы.")
            exit(1)
        return WEB_SERVER_HOST, WEB_SERVER_PORT

    WEB_SERVER_HOST, WEB_SERVER_PORT = set_WEB_SERVER_HOST_and_PORT()