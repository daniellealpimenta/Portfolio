from sqlalchemy import func
from sqlalchemy.orm import Session
from Models.user import User
from Schemas.user import UserUpdate
from uuid import UUID

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(func.lower(User.email) == email.strip().lower()).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(func.lower(User.username) == username.strip().lower()).first()
    
    def update(self, user_id: UUID, user_data: UserUpdate) -> User | None:
        usuario = self.get_by_id(user_id)
        if not usuario:
            return None
        
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(usuario, field, value)
        
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
    
    def delete(self, user_id: UUID) -> bool:
        usuario = self.get_by_id(user_id)
        if not usuario:
            return False
        
        self.db.delete(usuario)
        self.db.commit()
        return True