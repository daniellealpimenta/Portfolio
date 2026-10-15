from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from Core.database import get_db
from Core.limiter import limiter
import Models.user as user_model
from Services.email_service import send_contact_email_task

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)

class ContactFormRequest(BaseModel):
    user_id: UUID
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    subject: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=5000)

# Público, então limitado por IP pra ninguém usar o formulário pra encher o seu e-mail.
@router.post("/")
@limiter.limit("5/hour")
def submit_contact_form(request: Request, body: ContactFormRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Buscar o usuário pelo user_id para pegar o e-mail cadastrado dele
    user = db.query(user_model.User).filter(user_model.User.id == body.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário do portfólio não encontrado.")

    # Adicionar tarefa à BackgroundTasks do FastAPI
    background_tasks.add_task(
        send_contact_email_task,
        name=body.name,
        email=body.email,
        subject=body.subject,
        message_body=body.message,
        target_email=user.email
    )

    return {"message": "Sua mensagem foi recebida e está sendo enviada."}
