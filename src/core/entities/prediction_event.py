from typing import Literal

from pydantic import BaseModel


class PredictionEvent(BaseModel):
    job_id: str
    user_id: int
    model_name: Literal["linear_regression", "gradient_boosting", "random_forest"]
    created_at: str | None
    finished_at: str | None = None
    result: float | None = None
