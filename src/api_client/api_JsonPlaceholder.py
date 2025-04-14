from pydantic import BaseModel
from typing import List
import aiohttp

class UserModel(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone: str
    website: str

    class Config:
        alias_generator = lambda s: s.lower()  # Преобразует camelCase в snake_case

class JsonPlaceholderClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_users(self) -> List[UserModel]:
        async with self.session.get(f"{self.BASE_URL}/users") as response:
            data = await response.json()
            return [UserModel(**user) for user in data]