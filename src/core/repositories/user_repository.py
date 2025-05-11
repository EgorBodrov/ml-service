from abc import ABC, abstractmethod

from src.core.entities import User


class UserRepository(ABC):

    @abstractmethod
    async def save(self, user: User):
        pass

    @abstractmethod
    async def get(self, email: str) -> User | None:
        pass
