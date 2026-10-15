from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
import uuid
from Models.base import BaseORMModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Models.project import Project

class ProjectImage(BaseORMModel):
    __tablename__ = "project_image"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    image_path: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    # Relationship
    project: Mapped["Project"] = relationship("Project", back_populates="images")
