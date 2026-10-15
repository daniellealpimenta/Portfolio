from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import date
import uuid
from Models.base import BaseORMModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Models.user import User
    from Models.recommendation import Recommendation

class Experience(BaseORMModel):
    __tablename__ = "experience"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=True)
    position: Mapped[str] = mapped_column(nullable=False)
    company: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    exit_date: Mapped[date] = mapped_column(nullable=True)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="experiences")
    recommendations: Mapped[list["Recommendation"]] = relationship("Recommendation", back_populates="experience", cascade="all, delete-orphan", passive_deletes=True)
