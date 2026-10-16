from datetime import date, datetime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import mapped_column, Mapped, relationship
from Models.base import BaseORMModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Models.project import Project
    from Models.experience import Experience
    from Models.certificate import Certificate
    from Models.skill import Skill
    from Models.recommendation import Recommendation
    from Models.tool import Tool


class User(BaseORMModel):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    # Relaxados pra permitir cadastro enxuto (nome + username + email) — o resto
    # do perfil é preenchido depois pelo próprio usuário no /admin.
    description: Mapped[str] = mapped_column(nullable=True)
    birth_date: Mapped[date] = mapped_column(nullable=True)
    main_phrase: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    cellphone_number: Mapped[str] = mapped_column(nullable=True, unique=True)
    avatar_url: Mapped[str] = mapped_column(nullable=True)
    linkedin_url: Mapped[str] = mapped_column(nullable=True, unique=True)
    github_url: Mapped[str] = mapped_column(nullable=True, unique=True)
    medium_url: Mapped[str] = mapped_column(nullable=True, unique=True)
    instagram_url: Mapped[str] = mapped_column(nullable=True, unique=True)
    personality_test_url: Mapped[str] = mapped_column(nullable=True, unique=True)
    curriculum_url: Mapped[str] = mapped_column(nullable=True, unique=True)
    curriculum_en_url: Mapped[str] = mapped_column(nullable=True, unique=True)

    # Links do perfil que o admin escolheu esconder do site público
    # (nomes de campo, ex: ["instagram_url"]). A API pública manda esses campos vazios.
    hidden_fields: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list, server_default="{}")

    # Login por código (passwordless) — código de uso único, com hash e expiração
    login_code_hash: Mapped[str] = mapped_column(nullable=True)
    login_code_expires_at: Mapped[datetime] = mapped_column(nullable=True)

    # Relationships
    projects: Mapped[list["Project"]] = relationship("Project", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    skills: Mapped[list["Skill"]] = relationship("Skill", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    experiences: Mapped[list["Experience"]] = relationship("Experience", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    certificates: Mapped[list["Certificate"]] = relationship("Certificate", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    recommendations: Mapped[list["Recommendation"]] = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    tools: Mapped[list["Tool"]] = relationship("Tool", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
