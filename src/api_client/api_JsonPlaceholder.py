from typing import List
import aiohttp

from src.models import UserPydantic


class JsonPlaceholderClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_users(self) -> List[UserPydantic]:
        async with self.session.get(f"{self.BASE_URL}/users") as response:
            data = await response.json()
            return [UserPydantic(**user) for user in data]
