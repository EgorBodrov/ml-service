from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.infrastructure.web.controllers.user_balance_controller import router as user_balance_router
from src.infrastructure.web.controllers.predictor_controller import router as model_router
from src.infrastructure.web.controllers.user_controller import router as user_router
from src.infrastructure.db.models.base import Base
from src.infrastructure.db.utils import engine

from src.infrastructure.db.repositories import PredictorRepositoryImpl
from src.infrastructure.db.utils import async_session
from src.core.use_cases import PredictorUseCases


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        repo = PredictorRepositoryImpl(session)
        models = await PredictorUseCases(repo).get_all()
        if not models:
            await PredictorUseCases(repo).create("linear_regression", 10)
            await PredictorUseCases(repo).create("gradient_boosting", 25)
            await PredictorUseCases(repo).create("random_forest", 40)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(user_balance_router, prefix="/api/v1", tags=["balances"])
app.include_router(model_router, prefix="/api/v1", tags=["models"])
