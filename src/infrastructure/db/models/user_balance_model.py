from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer

from src.infrastructure.db.models import Base


class UserBalanceModel(Base):
    __tablename__ = "balances"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, primary_key=True)
    amount: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("UserModel", back_populates="balance")
