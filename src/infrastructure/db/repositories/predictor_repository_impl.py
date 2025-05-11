from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.infrastructure.db.models import PredictorModel
from src.core.repositories import PredictorRepository
from src.core.entities import Predictor


class PredictorRepositoryImpl(PredictorRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, predictor: Predictor) -> Predictor:
        predictor_model = PredictorModel(
            model_name=predictor.model_name,
            price=predictor.price
        )
        self.session.add(predictor_model)
        await self.session.commit()
        await self.session.refresh(predictor_model)
        return Predictor(
            model_name=predictor_model.model_name,
            price=predictor_model.price
        )

    async def get(self, model_name: str) -> Predictor | None:
        result = await self.session.execute(select(PredictorModel).where(PredictorModel.model_name == model_name))
        predictor_model = result.scalar_one_or_none()
        if predictor_model:
            return Predictor(
                model_name=predictor_model.model_name,
                price=predictor_model.price
            )
        return None
    
    async def get_all(self):
        result = await self.session.execute(select(PredictorModel))
        predictor_models = result.scalars().all()
        return [
            Predictor(
                model_name=p.model_name,
                price=p.price
            )
            for p in predictor_models
        ]
