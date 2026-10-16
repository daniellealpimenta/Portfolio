from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class RequestCodeOut(BaseModel):
    detail: str


# Portfólio de um usuário só: o código sempre vai pro ADMIN_EMAIL do .env,
# então o login não pede e-mail, só o código.
class VerifyCodeIn(BaseModel):
    code: str = Field(min_length=6, max_length=6)


class AuthUserOut(BaseModel):
    id: UUID
    name: str
    username: str | None
    email: str

    model_config = ConfigDict(from_attributes=True)
