import os

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from Core.database import get_db
from Core.deps import SESSION_COOKIE_NAME, get_current_user
from Core.limiter import limiter
from Core.security import SESSION_MAX_AGE_SECONDS
from Models.user import User
from Schemas.auth import AuthUserOut, RequestCodeIn, RequestCodeOut, VerifyCodeIn
from Schemas.user import UserResponse
from Services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

# True em produção (HTTPS). Em dev local (http://localhost) precisa ser False,
# senão o navegador descarta o cookie.
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"


@router.post("/request-code", response_model=RequestCodeOut)
@limiter.limit("5/minute")
def request_code(request: Request, body: RequestCodeIn, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.request_code(body.email)


@router.post("/verify-code", response_model=AuthUserOut)
@limiter.limit("10/minute")
def verify_code(request: Request, body: VerifyCodeIn, response: Response, db: Session = Depends(get_db)):
    service = AuthService(db)
    token, user = service.verify_code(body.email, body.code)

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        max_age=SESSION_MAX_AGE_SECONDS,
        httponly=True,
        samesite="lax",
        secure=COOKIE_SECURE,
        path="/",
    )
    return user


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    # Endpoint autenticado — só devolve dados de quem está logado, por isso
    # pode incluir o perfil completo (e-mail, telefone), diferente do
    # GET /users/{identifier} público, que é enxuto de propósito.
    return current_user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE_NAME, path="/", samesite="lax", secure=COOKIE_SECURE)
    return {"detail": "Sessão encerrada."}
