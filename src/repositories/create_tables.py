import logging

from sqlalchemy import MetaData, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import declarative_base

from src.models import Base

#Лучше использовать миграции через алембик, но в тз не упоминяется


async def safe_create_tables(engine: AsyncEngine):
    """Безопасное создание таблиц с обработкой ошибок"""
    metadata = Base.metadata
    try:
        async with engine.begin() as conn:
            existing_before = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names()
            )

            await conn.run_sync(metadata.create_all, checkfirst=True)

            existing_after = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names()
            )
            created_tables = set(existing_after) - set(existing_before)

            if created_tables:
                print(f"Созданы таблицы: {', '.join(created_tables)}")
            else:
                print(f"Все таблицы уже существуют: {', '.join(existing_after)}")

    except SQLAlchemyError as e:
        logging.error(f"Ошибка при создании таблиц: {e}")
        raise
