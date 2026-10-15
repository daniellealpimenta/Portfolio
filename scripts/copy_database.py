"""
Copia todos os dados de um Postgres (ex: Supabase) para o banco do DATABASE_URL (ex: Neon).

Uso (uma vez, na migração):
    1. Crie as tabelas no destino:   uv run alembic upgrade head
    2. Copie os dados:               uv run python -m scripts.copy_database "<URL do Supabase>"

A URL de origem é a "Session pooler" ou "Direct connection" do painel do Supabase
(Project Settings > Database). O destino precisa estar vazio; o script não apaga nada.
Use --dry-run pra só contar as linhas.
"""
import argparse
import sys

from sqlalchemy import MetaData, create_engine, func, select

from Core.database import Base, engine as target_engine
import Models.user  # noqa: F401  (registra as tabelas no Base.metadata)
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


def normalize_url(url: str) -> str:
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return url.replace(prefix, "postgresql+psycopg2://", 1)
    return url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source_url", help="URL do banco de origem (Supabase)")
    parser.add_argument("--dry-run", action="store_true", help="só mostra quantas linhas seriam copiadas")
    args = parser.parse_args()

    source_engine = create_engine(normalize_url(args.source_url), connect_args={"connect_timeout": 15})

    if source_engine.url.host == target_engine.url.host and source_engine.url.database == target_engine.url.database:
        print("Origem e destino são o mesmo banco — confira o DATABASE_URL no .env.")
        return 1

    # Lê a estrutura real da origem: se algum campo novo ainda não existir lá,
    # ele é simplesmente pulado (fica com o default/NULL no destino).
    source_meta = MetaData()
    source_meta.reflect(bind=source_engine)

    # sorted_tables já vem na ordem das foreign keys (user antes de project, etc.)
    tables = Base.metadata.sorted_tables

    with source_engine.connect() as src, target_engine.begin() as dst:
        for table in tables:
            if table.name not in source_meta.tables:
                print(f"  {table.name:<16} não existe na origem, pulando")
                continue
            existing = dst.execute(select(func.count()).select_from(table)).scalar_one()
            if existing:
                print(f"O destino já tem {existing} linha(s) em '{table.name}'. Use um banco vazio.")
                return 1

        total = 0
        for table in tables:
            if table.name not in source_meta.tables:
                continue
            src_table = source_meta.tables[table.name]
            columns = [c.name for c in table.columns if c.name in src_table.columns]
            rows = [dict(r._mapping) for r in src.execute(select(*[src_table.c[c] for c in columns]))]
            print(f"  {table.name:<16} {len(rows):>5} linha(s)")
            if rows and not args.dry_run:
                dst.execute(table.insert(), rows)
            total += len(rows)

        if args.dry_run:
            dst.rollback()
            print(f"\n[dry-run] {total} linha(s) seriam copiadas. Nada foi gravado.")
            return 0

    # Confere se o destino ficou com o mesmo número de linhas da origem
    ok = True
    with source_engine.connect() as src, target_engine.connect() as dst:
        for table in tables:
            if table.name not in source_meta.tables:
                continue
            a = src.execute(select(func.count()).select_from(source_meta.tables[table.name])).scalar_one()
            b = dst.execute(select(func.count()).select_from(table)).scalar_one()
            if a != b:
                ok = False
                print(f"  DIFERENÇA em {table.name}: origem={a} destino={b}")

    print(f"\n{total} linha(s) copiadas." if ok else "\nA cópia terminou com diferenças, veja acima.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
