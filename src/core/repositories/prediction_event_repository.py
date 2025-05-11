from abc import ABC, abstractmethod

from src.core.entities import PredictionEvent


class PredictionEventRepository(ABC):

    @abstractmethod
    async def save(self, event: PredictionEvent):
        pass

    @abstractmethod
    async def get(self, job_id: str) -> PredictionEvent | None:
        pass

    @abstractmethod
    async def set_result(self, job_id: str, result: float) -> PredictionEvent | None:
        pass

    @abstractmethod
    async def get_all(self, user_id: int) -> list[str]:
        pass
