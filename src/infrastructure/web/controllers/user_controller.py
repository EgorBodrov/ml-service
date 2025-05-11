from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.infrastructure.db.repositories import UserRepositoryImpl
from src.infrastructure.db.utils import get_session
from src.core.use_cases import UserUseCases
from src.infrastructure.web.models import (
    SignUpUserResponse,
    SignInUserResponse,
    SignUpUserRequest,
    SignInUserRequest
)


router = APIRouter()

@router.post("/sign_up", response_model=SignUpUserResponse)
async def sign_up_user(request: SignUpUserRequest, session: AsyncSession = Depends(get_session)):
    repository = UserRepositoryImpl(session)
    try:
        user = await UserUseCases(repository).sign_up(
            request.name,
            request.email,
            request.password
        )
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return SignUpUserResponse.model_validate({"name": user.name, "email": user.email})


@router.post("/sign_in", response_model=SignInUserResponse)
async def sign_in_user(request: SignInUserRequest, session: AsyncSession = Depends(get_session)):
    repo = UserRepositoryImpl(session)
    try:
        data = await UserUseCases(repo).sign_in(request.email, request.password)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if not data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return SignInUserResponse.model_validate(data)
