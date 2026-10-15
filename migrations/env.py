from logging.config import fileConfig

from alembic import context

# Importar o Core.database carrega o .env e monta o engine a partir do DATABASE_URL
from Core.database import Base, engine
import Models.user  # noqa: F401  (registra todas as tabelas no Base.metadata)
import Models.project  # noqa: F401
import Models.project_image  # noqa: F401
import Models.project_link  # noqa: F401
import Models.project_like  # noqa: F401
import Models.tool  # noqa: F401
import Models.associations  # noqa: F401
import Models.certificate  # noqa: F401
import Models.experience  # noqa: F401
import Models.skill  # noqa: F401
import Models.recommendation  # noqa: F401
import Models.stored_file  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Gera o SQL sem conectar (alembic upgrade head --sql)."""
    context.configure(
        url=engine.url.render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
