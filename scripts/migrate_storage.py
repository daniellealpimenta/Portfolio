"""
Traz os arquivos do Supabase Storage para dentro do banco (tabela stored_file) e atualiza as URLs.

Procura, em todas as colunas de texto de todas as tabelas do DATABASE_URL, URLs públicas
do Supabase Storage (".../storage/v1/object/public/<bucket>/<caminho>"), baixa cada arquivo,
salva no banco e troca a URL pelo caminho /files/<id>.<ext>.

Uso (depois do copy_database, com o Supabase ainda ativo):
    uv run python -m scripts.migrate_storage --dry-run   # só lista o que faria
    uv run python -m scripts.migrate_storage
"""
import argparse
import mimetypes
import re
import sys
import urllib.request

from sqlalchemy import String, select, update
from sqlalchemy.orm import Session

from Core.database import Base, engine
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
from Services.storage_service import EXTENSIONS, MAX_UPLOAD_BYTES, file_path, save_file

SUPABASE_PUBLIC_RE = re.compile(r"^https://[^/]+\.supabase\.co/storage/v1/object/public/[^/]+/(?P<path>[^?#]+)")


def download(url: str) -> tuple[bytes, str]:
    with urllib.request.urlopen(url, timeout=60) as resp:
        content_type = resp.headers.get_content_type()
        data = resp.read(MAX_UPLOAD_BYTES * 3)
    if content_type not in EXTENSIONS:
        content_type = mimetypes.guess_type(url)[0] or content_type
    if content_type == "image/jpg":
        content_type = "image/jpeg"
    return data, content_type


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="só lista os arquivos, sem baixar nem alterar o banco")
    args = parser.parse_args()

    copied: dict[str, str] = {}  # URL antiga -> caminho novo (o mesmo arquivo pode aparecer em várias linhas)
    failures = 0

    with Session(engine) as db:
        for table in Base.metadata.sorted_tables:
            if table.name == "stored_file":
                continue
            text_columns = [c for c in table.columns if isinstance(c.type, String)]
            if not text_columns:
                continue
            for row in db.execute(select(table.c.id, *text_columns)).all():
                changes = {}
                for col in text_columns:
                    value = getattr(row, col.name)
                    match = SUPABASE_PUBLIC_RE.match(value) if isinstance(value, str) else None
                    if not match:
                        continue
                    if value not in copied:
                        key = urllib.request.unquote(match.group("path"))
                        print(f"  {table.name}.{col.name}: {key}")
                        if args.dry_run:
                            copied[value] = "(dry-run)"
                        else:
                            try:
                                data, content_type = download(value)
                                if content_type not in EXTENSIONS:
                                    raise ValueError(f"tipo de arquivo não suportado: {content_type}")
                                folder = key.split("/", 1)[0] if "/" in key else "misc"
                                copied[value] = file_path(save_file(db, data, content_type, folder))
                            except Exception as e:
                                failures += 1
                                print(f"    ERRO: {e} (a URL antiga foi mantida)")
                                continue
                    changes[col.name] = copied[value]
                if changes and not args.dry_run:
                    db.execute(update(table).where(table.c.id == row.id).values(**changes))
        if not args.dry_run:
            db.commit()

    verb = "seriam copiados" if args.dry_run else "copiados para o banco"
    print(f"\n{len(copied)} arquivo(s) {verb}." + (f" {failures} falha(s)." if failures else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
