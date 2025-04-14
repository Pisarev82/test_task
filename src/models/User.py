from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


# sqlalchemy
Base = declarative_base()

class UserSQLAlchemy(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    phone = Column(String)
    website = Column(String)

    @staticmethod
    def to_pydantic(self):
        return UserPyDantic(
            id=self.id,
            name=self.name,
            username=self.username,
            email=self.email,
            phone=self.phone,
            website=self.website
        )


#pydantic
class UserPyDantic (BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    name: str
    username: str
    email: str
    phone: str
    website: str

    @staticmethod
    def to_db(self):
        return UserSQLAlchemy(
            name=self.name,
            username=self.username,
            email=self.email,
            phone=self.phone,
            website=self.website
        )

    @staticmethod
    def camel_to_snake(name: str) -> str:
        """Преобразование camelCase в snake_case"""
        result = []
        for i, char in enumerate(name):
            if char.isupper() and i > 0:
                result.append('_')
            result.append(char.lower())
        return ''.join(result)

    model_config = ConfigDict(
        alias_generator=camel_to_snake,
        populate_by_field_name=True,      # Разрешаем использовать оба варианта имен
    )

