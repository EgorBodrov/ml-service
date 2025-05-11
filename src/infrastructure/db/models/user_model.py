from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer

from src.infrastructure.db.models import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)

    balance = relationship("UserBalanceModel", uselist=False, back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("PredictionEventModel", back_populates="user", cascade="all, delete-orphan")
