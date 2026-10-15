from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from Models.base import BaseORMModel
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from Models.project import Project
    from Models.user import User

class Tool(BaseORMModel):
    __tablename__ = "tool"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    icon_url: Mapped[str] = mapped_column(nullable=True)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="tools")
    projects: Mapped[list["Project"]] = relationship(secondary="project_tool", back_populates="tools")