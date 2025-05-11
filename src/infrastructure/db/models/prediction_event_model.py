from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey

from src.infrastructure.db.models import Base


class PredictionEventModel(Base):
    __tablename__ = "prediction_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)
    job_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)
    finished_at: Mapped[str] = mapped_column(String(50), nullable=True)
    result: Mapped[float] = mapped_column(Float, nullable=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=False, nullable=False)
    user = relationship("UserModel", back_populates="tasks")
