from abc import ABC, abstractmethod
from typing import List

from src.core.entities import Predictor


class PredictorRepository(ABC):

    @abstractmethod
    async def save(self, predictor: Predictor):
        pass

    @abstractmethod
    async def get(self, model_name: str) -> Predictor | None:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Predictor] | None:
        pass
