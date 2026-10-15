from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import date
import uuid
from Models.base import BaseORMModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Models.user import User

class Certificate(BaseORMModel):
    __tablename__ = "certificate"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name_course: Mapped[str] = mapped_column(nullable=False)
    plataform: Mapped[str] = mapped_column(nullable=False)
    workload: Mapped[int] = mapped_column(nullable=False)
    issue_date: Mapped[date] = mapped_column(nullable=False)
    digital_certificate_url: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="certificates")