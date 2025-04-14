from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.User import UserPyDantic, UserSQLAlchemy
import logging


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_users(self, users: list[UserPyDantic]):

        if not users:
            return 0

        users_sqlalchemy = [UserPyDantic.to_db(user) for user in users]
        users_data_for_insert = [user.model_dump() for user in users]
        set_cols_for_update = [col for col in users_sqlalchemy[0].keys() if col != 'id']

        try:
            logging.info("Saving user in PostgreSQL...")
            stmt = insert(UserSQLAlchemy) \
                .values(users_data_for_insert) \
                .on_conflict_do_update(
                index_elements=['id'],
                set_=set_cols_for_update
            )

            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount

        except Exception as e:
            await self.session.rollback()
            logging.error(f"Database error: {e}")
            return 0

