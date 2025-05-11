from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.infrastructure.db.models import PredictionEventModel
from src.core.repositories import PredictionEventRepository
from src.core.entities import PredictionEvent


class PredictionEventRepositoryImpl(PredictionEventRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, event: PredictionEvent) -> PredictionEvent:
        event_model = PredictionEventModel(
            model_name=event.model_name,
            job_id=event.job_id,
            user_id=event.user_id,
            created_at=event.created_at,
        )
        self.session.add(event_model)
        await self.session.commit()
        await self.session.refresh(event_model)
        return event

    async def get(self, job_id: str) -> PredictionEvent | None:
        result = await self.session.execute(select(PredictionEventModel).where(PredictionEventModel.job_id == job_id))
        predictor_model = result.scalar_one_or_none()
        if predictor_model:
            return PredictionEvent(
                model_name=predictor_model.model_name,
                job_id=predictor_model.job_id,
                user_id=predictor_model.user_id,
                created_at=predictor_model.created_at,
                finished_at=predictor_model.finished_at,
                result=predictor_model.result
            )
        return None
    
    async def set_result(self, job_id: str, result: float) -> PredictionEvent:
        event = await self._get_model_by_job_id(job_id=job_id)
        if not event:
            return None
        
        event.result = result
        event.finished_at = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        await self.session.commit()
        await self.session.refresh(event)
        return PredictionEvent(
            model_name=event.model_name,
            job_id=event.job_id,
            user_id=event.user_id,
            created_at=event.created_at,
            finished_at=event.finished_at,
            result=event.result
        )

    async def _get_model_by_job_id(self, job_id: str) -> PredictionEventModel | None:
        result = await self.session.execute(select(PredictionEventModel).where(PredictionEventModel.job_id == job_id))
        return result.scalar_one_or_none()
    
    async def get_all(self, user_id: int) -> list[str]:
        results = await self.session.execute(select(PredictionEventModel.job_id).where(PredictionEventModel.user_id == user_id))
        results = results.scalars().all()
        return results
