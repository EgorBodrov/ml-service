from src.utils import hash_password, verify_password, create_access_token
from src.core.repositories import UserRepository
from src.core.entities import User


class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository: UserRepository = user_repository

    async def sign_up(self, name: str, email: str, password: str) -> User:
        hashed_password = hash_password(password)
        user = User(id=None, name=name, email=email, hashed_password=hashed_password)

        return await self.user_repository.save(user)
    
    async def sign_in(self, email: str, password: str) -> str:
        user = await self.user_repository.get(email=email)
        if not user or not verify_password(password, user.hashed_password):
            return None

        token = create_access_token({"email": user.email, "name": user.name, "sub": str(user.id),})
        data = user.model_dump(include={"name", "email"})
        data.update({"token": token})
        return data
