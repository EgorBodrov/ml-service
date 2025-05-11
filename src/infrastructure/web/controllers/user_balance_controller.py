from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.web.models import UserBalanceResponse, UserBalanceRequest
from src.infrastructure.web.controllers.get_current_user import get_current_user
from src.infrastructure.db.repositories import UserBalanceRepositoryImpl
from src.infrastructure.db.utils import get_session
from src.core.use_cases import UserBalanceUseCases
from src.core.entities import User


router = APIRouter()


@router.get("/balance", response_model=UserBalanceResponse)
async def get_balance(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    repository = UserBalanceRepositoryImpl(session)
    try:
        user_balance = await UserBalanceUseCases(repository).get(user.id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return UserBalanceResponse.model_validate({"amount": user_balance.amount})


@router.post("/balance", response_model=UserBalanceResponse)
async def update_balance(
    request: UserBalanceRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    repo = UserBalanceRepositoryImpl(session)
    try:
        user_balance = await UserBalanceUseCases(repo).update(user.id, request.new_amount)
    except Exception as exc:
        import traceback
        print("ASD")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(exc))

    return UserBalanceResponse.model_validate({"amount": user_balance.amount})
