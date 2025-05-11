from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.infrastructure.db.models import UserModel, UserBalanceModel
from src.core.repositories import UserRepository
from src.core.entities import User


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> User:
        user_model = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            balance=UserBalanceModel(amount=0)
        )
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            hashed_password=user_model.hashed_password
        )

    async def get(self, email: str) -> User | None:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        user_model = result.scalar_one_or_none()
        if user_model:
            return User(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                hashed_password=user_model.hashed_password
            )
        return None
