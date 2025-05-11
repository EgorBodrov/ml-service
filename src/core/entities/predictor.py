from typing import Literal

from pydantic import BaseModel


class Predictor(BaseModel):
    model_name: Literal["linear_regression", "gradient_boosting", "random_forest"]
    price: int
