from typing import TYPE_CHECKING
from Models.base import BaseORMModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import date as Date
import uuid

if TYPE_CHECKING:
    from Models.user import User
    from Models.tool import Tool
    from Models.project_image import ProjectImage
    from Models.project_link import ProjectLink



class Project(BaseORMModel):
    __tablename__ = "project"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    # Um projeto pode pertencer a mais de uma categoria (ex: Mobile + GameDev).
    # Guardado como array de texto; os valores válidos são garantidos pelo enum
    # Category na camada de schema (Pydantic), não por constraint no banco.
    categories: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    likes: Mapped[int] = mapped_column(default=0, nullable=False)
    date: Mapped[Date] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="projects")
    tools: Mapped[list["Tool"]] = relationship(secondary="project_tool", back_populates="projects")
    images: Mapped[list["ProjectImage"]] = relationship("ProjectImage", back_populates="project", cascade="all, delete-orphan", passive_deletes=True)
    links: Mapped[list["ProjectLink"]] = relationship("ProjectLink", back_populates="project", cascade="all, delete-orphan", passive_deletes=True)