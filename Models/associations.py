from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from Models.base import BaseORMModel

class ProjectTool(BaseORMModel):
    __tablename__ = "project_tool"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    tool_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tool.id", ondelete="CASCADE"), nullable=False)