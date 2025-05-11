from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.infrastructure.db.models import UserModel, UserBalanceModel
from src.core.repositories import UserBalanceRepository
from src.core.entities import UserBalance


class UserBalanceRepositoryImpl(UserBalanceRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update(self, user_id: int, new_amount: int) -> UserBalance:
        user_balance_model = await self._get_model_by_user_id(user_id=user_id)
        if not user_balance_model:
            return None
        user_balance_model.amount = new_amount
        await self.session.commit()
        await self.session.refresh(user_balance_model)
        return UserBalance(
            user_id=user_balance_model.user_id,
            amount=user_balance_model.amount
        )

    async def get(self, user_id: int) -> UserBalance | None:
        user_balance_model = await self._get_model_by_user_id(user_id=user_id)
        if user_balance_model:
            return UserBalance(
                user_id=user_balance_model.user_id,
                amount=user_balance_model.amount
            )
        return None
    
    async def _get_model_by_user_id(self, user_id: int) -> UserBalanceModel | None:
        result = await self.session.execute(select(UserBalanceModel).where(UserBalanceModel.user_id == user_id))
        return result.scalar_one_or_none()
