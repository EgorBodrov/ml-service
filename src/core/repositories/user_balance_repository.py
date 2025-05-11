from abc import ABC, abstractmethod

from src.core.entities import UserBalance


class UserBalanceRepository(ABC):

    # @abstractmethod
    # async def save(self, user_balance: UserBalance):
    #     pass

    @abstractmethod
    async def update(self, user_id: int, new_amount: int):
        pass

    @abstractmethod
    async def get(self, user_id: int) -> UserBalance | None:
        pass
