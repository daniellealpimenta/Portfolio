from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from Core.security import validate_username
from Repositories.user import UserRepository
from Schemas.user import UserUpdate
from uuid import UUID

class UserService:
    def __init__(self, db: Session):
        # O Service instancia o Repository para poder usá-lo
        self.repository = UserRepository(db)

    def get_user_by_email(self, email: str):
        user = self.repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user

    def get_user_by_id(self, user_id: UUID):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user
    
    def get_user_by_identifier(self, identifier: str):
        try:
            # Tenta verificar se é um UUID válido
            user_uuid = UUID(identifier)
            user = self.repository.get_by_id(user_uuid)
        except ValueError:
            # Se não for UUID, assume que é username
            user = self.repository.get_by_username(identifier)
            
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user
    
    def update_user(self, user_id: UUID, user_data: UserUpdate):
        # O e-mail é o login do admin (ADMIN_EMAIL no .env) — trocar por aqui
        # trancaria o acesso, então só muda pelo .env + banco.
        if "email" in user_data.model_fields_set:
            current = self.get_user_by_id(user_id)
            if (user_data.email or "").lower() != current.email.lower():
                raise HTTPException(status_code=400, detail="O e-mail de acesso não pode ser alterado por aqui.")
            # Mesmo e-mail reenviado pelo formulário: só ignora
            user_data.model_fields_set.discard("email")

        if user_data.username is not None:
            user_data.username = user_data.username.strip().lower()
            username_error = validate_username(user_data.username)
            if username_error:
                raise HTTPException(status_code=400, detail=username_error)
            existing_user = self.repository.get_by_username(user_data.username)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=409, detail="Esse nome de usuário já está em uso.")

        try:
            updated_user = self.repository.update(user_id, user_data)
        except IntegrityError:
            self.repository.db.rollback()
            raise HTTPException(status_code=409, detail="Algum dos links informados já está em uso.")
        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return updated_user
    
    def delete_user(self, user_id: UUID):
        success = self.repository.delete(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"detail": "Usuário deletado com sucesso"}