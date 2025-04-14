from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import logging

from src.config import POSTGRES_URL


class Database:

    engine = create_async_engine(POSTGRES_URL, echo=True)
    session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Функция для получения сессии
    async def get_async_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session

    async def health_check(self):
        """Проверка подключения к БД"""
        try:
            async with self.engine.connect() as conn:
                await conn.execute("SELECT 1")
            return True
        except Exception as e:
            logging.error(f"Database health check failed: {e}")
            return False

db = Database()