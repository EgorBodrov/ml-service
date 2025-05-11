from typing import List

from src.core.repositories import PredictionEventRepository
from src.core.entities import PredictionEvent


class PredictionEventUseCases:
    def __init__(self, predictor_repository: PredictionEventRepository):
        self.predictor_repository: PredictionEventRepository = predictor_repository

    async def save(
        self,
        job_id: str,
        user_id: int,
        model_name: str,
        created_at: str,
    ) -> PredictionEvent:
        event = PredictionEvent(
            job_id=job_id,
            user_id=user_id,
            model_name=model_name,
            created_at=created_at
        )

        return await self.predictor_repository.save(event)
    
    async def get(self, job_id: str) -> PredictionEvent:
        event = await self.predictor_repository.get(job_id)
        if not event:
            return None

        return event

    async def set_result(self, job_id: str, result: float) -> PredictionEvent:
        event = await self.predictor_repository.set_result(job_id, result)
        if not event:
            return None

        return event
    
    async def get_all(self, user_id: int) -> list[str]:
        event = await self.predictor_repository.get_all(user_id)
        if not event:
            return None

        return event
