from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Uma única URL de conexão (ex: a string "pooled" do Neon).
# Ex: postgresql://usuario:senha@ep-xxx-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require
DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definida no .env — veja o .env.example.")

# O SQLAlchemy precisa do driver explícito; as strings do Neon vêm como "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# O Neon desliga o banco depois de alguns minutos sem uso e o pooler fecha
# conexões ociosas. pool_pre_ping testa a conexão antes de usar (e reconecta
# se ela tiver morrido); pool_recycle descarta conexões antigas antes disso.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=5,
    connect_args={"connect_timeout": 10},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
