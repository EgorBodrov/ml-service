from typing import Literal

from pydantic import BaseModel

from src.core.entities import Predictor


class PredictRequest(BaseModel):
    model_name: Literal["linear_regression", "gradient_boosting", "random_forest"]
    data: dict


class PredictResponse(BaseModel):
    job_id: str


class JobStatusRequest(BaseModel):
    job_id: str


class JobStatusResponse(BaseModel):
    status: str
    job_id: str
    model_name: Literal["linear_regression", "gradient_boosting", "random_forest"]
    created_at: str
    finished_at: str | None
    result: float | None


class PredictorsResponse(BaseModel):
    models: list[Predictor]


class EventsResponse(BaseModel):
    job_ids: list[str]
