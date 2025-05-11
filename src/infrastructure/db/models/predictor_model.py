from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from src.infrastructure.db.models import Base


class PredictorModel(Base):
    __tablename__ = "predictors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    model_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
