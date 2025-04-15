import logging

import gspread
from google.oauth2.service_account import Credentials

from src.models import UserSQLAlchemy


class GoogleSheetsExporter:
    def __init__(self, creds_file: str):
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = Credentials.from_service_account_file(creds_file, scopes=self.scope)
        self.client = gspread.authorize(self.creds)

    async def export_users(self, users: list[UserSQLAlchemy], spreadsheet_id: str):
        try:
            sheet = self.client.open_by_key(spreadsheet_id).sheet1
            data = [
                ["ID", "Name", "Username", "Email", "Phone", "Website"],
                *[[u.id, u.name, u.username, u.email, u.phone, u.website] for u in users]
            ]
            sheet.clear()
            sheet.update(data)
            return True
        except Exception as e:
            logging.error(f"Google Sheets Error: {e}")
            raise