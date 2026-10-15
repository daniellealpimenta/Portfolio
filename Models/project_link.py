from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
import uuid
from Models.base import BaseORMModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Models.project import Project

class ProjectLink(BaseORMModel):
    __tablename__ = "project_link"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    icon: Mapped[str] = mapped_column(nullable=False)

    # Relationship
    project: Mapped["Project"] = relationship("Project", back_populates="links")
