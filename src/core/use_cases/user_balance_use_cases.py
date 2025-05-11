from src.core.repositories import UserBalanceRepository
from src.core.entities import UserBalance


class UserBalanceUseCases:
    def __init__(self, user_balance_repository: UserBalanceRepository):
        self.user_balance_repository: UserBalanceRepository = user_balance_repository

    async def update(self, user_id: int, new_amount: int) -> UserBalance:
        return await self.user_balance_repository.update(user_id, new_amount)

    async def get(self, user_id: int) -> UserBalance:
        user_balance = await self.user_balance_repository.get(user_id=user_id)
        if not user_balance:
            return None

        return user_balance
