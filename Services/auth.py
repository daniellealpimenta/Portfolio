import os
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from Core.security import (
    create_session_token,
    generate_login_code,
    hash_login_code,
    login_code_expiry,
    verify_login_code,
)
from Models.user import User
from Repositories.user import UserRepository
from Services.email_service import EmailDeliveryError, send_login_code_email

# Portfólio de um usuário só: o único e-mail que pode entrar no /admin.
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "").strip().lower()
if not ADMIN_EMAIL:
    print("AVISO: ADMIN_EMAIL não definido no .env — ninguém conseguirá entrar no /admin.")

# Resposta idêntica pra qualquer e-mail, pra não revelar quais e-mails existem.
REQUEST_CODE_RESPONSE = {"detail": "Se esse e-mail tiver acesso, um código foi enviado para ele."}


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def request_code(self, email: str) -> dict:
        if not ADMIN_EMAIL or email.strip().lower() != ADMIN_EMAIL:
            return REQUEST_CODE_RESPONSE

        user = self.repository.get_by_email(ADMIN_EMAIL)
        if not user:
            return REQUEST_CODE_RESPONSE

        code = generate_login_code()
        user.login_code_hash = hash_login_code(code)
        user.login_code_expires_at = login_code_expiry()
        self.db.commit()

        # Enviado de forma síncrona (não em BackgroundTask) pra que uma falha de
        # SMTP apareça como erro no login, em vez de "código enviado" sem e-mail.
        try:
            send_login_code_email(target_email=user.email, code=code)
        except EmailDeliveryError:
            raise HTTPException(status_code=503, detail="Não foi possível enviar o e-mail agora. Tente novamente em instantes.")

        return REQUEST_CODE_RESPONSE

    def verify_code(self, email: str, code: str) -> tuple[str, User]:
        user = self.repository.get_by_email(email)
        if not user or not user.login_code_hash or not user.login_code_expires_at:
            raise HTTPException(status_code=401, detail="Código inválido ou expirado.")

        expires_at = user.login_code_expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if datetime.now(timezone.utc) > expires_at or not verify_login_code(code, user.login_code_hash):
            raise HTTPException(status_code=401, detail="Código inválido ou expirado.")

        # Código de uso único: invalida assim que verificado, mesmo com sucesso
        user.login_code_hash = None
        user.login_code_expires_at = None
        self.db.commit()

        token = create_session_token(user.id)
        return token, user
