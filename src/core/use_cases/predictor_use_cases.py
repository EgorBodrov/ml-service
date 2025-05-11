from typing import List

from src.core.repositories import PredictorRepository
from src.core.entities import Predictor


class PredictorUseCases:
    def __init__(self, predictor_repository: PredictorRepository):
        self.predictor_repository: PredictorRepository = predictor_repository

    async def create(self, model_name: str, price: int) -> Predictor:
        predictor = Predictor(model_name=model_name, price=price)

        return await self.predictor_repository.save(predictor)
    
    async def get(self, model_name: str) -> Predictor:
        predictor = await self.predictor_repository.get(model_name)
        if not predictor:
            return None

        return predictor
    
    async def get_all(self) -> List[Predictor]:
        predictors = await self.predictor_repository.get_all()
        if not predictors:
            return None

        return predictors
