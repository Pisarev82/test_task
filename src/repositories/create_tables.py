import logging

from sqlalchemy import MetaData, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine


#Лучше использовать миграции через алембик, но в тз не упоминяется


async def safe_create_tables(engine: AsyncEngine):
    """Безопасное создание таблиц с обработкой ошибок"""
    try:
        async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all, checkfirst=True)
                logging.info("Таблицы созданы успешно")
    except SQLAlchemyError as e:
        logging.error(f"Ошибка при создании таблиц: {e}")
        raise

metadata = MetaData()
