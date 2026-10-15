from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
import uuid
from Models.base import BaseORMModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Models.user import User

class Skill(BaseORMModel):
    __tablename__ = "skill"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    icon_url: Mapped[str] = mapped_column(nullable=True)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="skills")