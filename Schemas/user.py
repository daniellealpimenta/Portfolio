from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from typing import Literal, Optional, List
from datetime import date as Date, datetime
from uuid import UUID

# Campos do perfil que podem ser escondidos do site público pelo admin
HideableField = Literal[
    "linkedin_url", "github_url", "instagram_url", "medium_url",
    "personality_test_url", "curriculum_url", "curriculum_en_url",
]


class UserBase(BaseModel):
    name: str
    username: Optional[str] = None
    description: Optional[str] = None
    birth_date: Optional[Date] = None
    main_phrase: Optional[str] = None
    email: EmailStr
    cellphone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    medium_url: Optional[str] = None
    instagram_url: Optional[str] = None
    personality_test_url: Optional[str] = None
    curriculum_url: Optional[str] = None
    curriculum_en_url: Optional[str] = None
    hidden_fields: List[str] = Field(default_factory=list)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    description: Optional[str] = None
    birth_date: Optional[Date] = None
    main_phrase: Optional[str] = None
    email: Optional[EmailStr] = None
    cellphone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    medium_url: Optional[str] = None
    instagram_url: Optional[str] = None
    personality_test_url: Optional[str] = None
    curriculum_url: Optional[str] = None
    curriculum_en_url: Optional[str] = None
    hidden_fields: Optional[List[HideableField]] = None

class UserResponse(UserBase):
    id: UUID

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserPublicResponse(BaseModel):
    """Versão exposta publicamente (páginas do portfólio) — sem e-mail.
    cellphone_number fica incluído de propósito: é usado no botão de
    contato via WhatsApp no site público."""
    id: UUID
    name: str
    username: Optional[str] = None
    description: Optional[str] = None
    main_phrase: Optional[str] = None
    cellphone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    medium_url: Optional[str] = None
    instagram_url: Optional[str] = None
    personality_test_url: Optional[str] = None
    curriculum_url: Optional[str] = None
    curriculum_en_url: Optional[str] = None
    created_at: datetime
    # Lido do banco só pra esconder os campos abaixo; não vai na resposta
    hidden_fields: List[str] = Field(default_factory=list, exclude=True)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def _hide_fields(self):
        # O link escondido nem sai do servidor (não basta escondê-lo na página)
        for name in self.hidden_fields:
            if name in type(self).model_fields and name != "hidden_fields":
                setattr(self, name, None)
        return self
