import os

from dotenv import load_dotenv

# Carrega o .env antes de qualquer módulo que leia variáveis de ambiente na importação
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from Core.limiter import limiter
import Models.base
import Models.user        
import Models.project     
import Models.project_image
import Models.project_link
import Models.project_like
import Models.tool
import Models.associations
import Models.certificate
import Models.experience
import Models.skill
import Models.recommendation
import Models.stored_file

from Routes.auth import router as auth_router
from Routes.project import router as project_router
from Routes.user import router as user_router
from Routes.project_image import router as project_image_router
from Routes.project_link import router as project_link_router
from Routes.skill import router as skill_router
from Routes.tool import router as tool_router
from Routes.experience import router as experience_router
from Routes.certificate import router as certificate_router
from Routes.recommendation import router as recommendation_router
from Routes.contact import router as contact_router
from Routes.system import router as system_router
from Routes.resume_analysis import router as resume_analysis_router
from Routes.uploads import router as uploads_router

# O schema do banco é gerenciado pelo Alembic (alembic upgrade head), não aqui.

app = FastAPI(
    title="Portfolio API",
    description="API do meu portfólio pessoal (FastAPI + Postgres no Neon)",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Habilitar CORS para o Frontend (Navegador)
# Precisa ser uma lista explícita (não "*") porque o login usa cookie de sessão
# com credenciais — navegadores recusam cookies em respostas com
# Access-Control-Allow-Origin: "*" quando allow_credentials é True.
_default_origins = "http://localhost:3000,http://127.0.0.1:3000"
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", _default_origins).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(project_image_router)
app.include_router(project_link_router)
app.include_router(skill_router)
app.include_router(tool_router)
app.include_router(experience_router)
app.include_router(certificate_router)
app.include_router(recommendation_router)
app.include_router(contact_router)
app.include_router(system_router)
app.include_router(resume_analysis_router)
app.include_router(uploads_router)

@app.get("/")
def read_root():
    return {"message": "Servidor do Portfólio está rodando perfeitamente!"}