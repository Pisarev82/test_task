from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.User import UserPydantic, UserSQLAlchemy
import logging


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_users(self, users: list[UserPydantic]):

        if not users:
            return 0

        try:
            # Преобразуем Pydantic модели в словари
            users_data = [user.model_dump() for user in users]

            # Получаем список полей для обновления (все кроме id)
            columns_to_update = list(users_data[0].keys())
            columns_to_update.remove('id')  # Исключаем первичный ключ

            # Создаем выражение для UPSERT
            stmt = insert(UserSQLAlchemy).values(users_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=['id'],
                set_={col: getattr(stmt.excluded, col) for col in columns_to_update}
            )

            # Выполняем запрос
            result = await self.session.execute(stmt)
            await self.session.commit()

            return result.rowcount

        except Exception as e:
            await self.session.rollback()
            logging.error(f"Database error: {e}", exc_info=True)
            return 0

