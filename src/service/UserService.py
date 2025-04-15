import logging

from src.api_client import JsonPlaceholderClient
from src.repositories import UserRepository


class UserService:
    def __init__(
            self,
            api_client: JsonPlaceholderClient,
            user_repo: UserRepository
    ):
        self.api = api_client
        self.repo = user_repo


    async def export_to_gsheets(self, spreadsheet_id: str):
        """Экспорт пользователей в Google Sheets"""
        try:
            users = await self.repo.get_all_users()
            # Реализация экспорта...
            return True
        except Exception as e:
            logging.error(f"Export Error: {e}")
            raise