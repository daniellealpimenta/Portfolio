from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, UniqueConstraint
import uuid
from Models.base import BaseORMModel


class ProjectLike(BaseORMModel):
    __tablename__ = "project_like"
    __table_args__ = (
        UniqueConstraint("project_id", "visitor_id", name="uq_project_like_project_visitor"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    # Identificador anônimo persistido num cookie no navegador do visitante —
    # não há login de visitante público, então é o jeito de saber "quem" já curtiu.
    visitor_id: Mapped[str] = mapped_column(nullable=False)
