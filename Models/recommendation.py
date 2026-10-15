from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import date as Date
import uuid
from Models.base import BaseORMModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Models.user import User
    from Models.experience import Experience

class Recommendation(BaseORMModel):
    __tablename__ = "recommendation"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    experience_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("experience.id", ondelete="CASCADE"), nullable=False)
    name_recommender: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    linkedin_recommender_url: Mapped[str] = mapped_column(nullable=True)
    recommender_avatar_url: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[Date] = mapped_column(nullable=True)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="recommendations")
    experience: Mapped["Experience"] = relationship("Experience", back_populates="recommendations")

