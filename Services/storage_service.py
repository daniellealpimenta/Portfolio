import re
from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from Models.stored_file import StoredFile

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB

IMAGE_TYPES = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "image/gif": "gif"}
PDF_TYPES = {"application/pdf": "pdf"}

# Pasta -> tipos aceitos (mesmas pastas que o bucket do Supabase usava)
FOLDERS = {
    "avatars": IMAGE_TYPES,
    "curriculums": PDF_TYPES,
    "tests": PDF_TYPES,
}

EXTENSIONS = {**IMAGE_TYPES, **PDF_TYPES}

# Assinatura dos primeiros bytes, pra não confiar só no Content-Type do navegador
MAGIC_BYTES = {
    "jpg": [b"\xff\xd8\xff"],
    "png": [b"\x89PNG\r\n\x1a\n"],
    "gif": [b"GIF87a", b"GIF89a"],
    "webp": [b"RIFF"],
    "pdf": [b"%PDF"],
}

# Caminho guardado no banco (relativo, pra não depender do domínio da API)
FILE_PATH_RE = re.compile(r"^/files/(?P<id>[0-9a-fA-F-]{36})\.(?P<ext>[a-z]+)$")


def file_path(stored: StoredFile) -> str:
    return f"/files/{stored.id}.{EXTENSIONS[stored.content_type]}"


def save_file(db: Session, data: bytes, content_type: str, folder: str) -> StoredFile:
    stored = StoredFile(folder=folder, content_type=content_type, size=len(data), data=data)
    db.add(stored)
    db.commit()
    db.refresh(stored)
    return stored


def upload_file(db: Session, file: UploadFile, folder: str) -> str:
    """Valida e salva o arquivo no banco. Retorna o caminho /files/<id>.<ext>."""
    allowed = FOLDERS.get(folder)
    if allowed is None:
        raise HTTPException(status_code=400, detail=f"Pasta inválida. Use uma de: {', '.join(FOLDERS)}.")

    ext = allowed.get(file.content_type or "")
    if not ext:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido para essa pasta.")

    data = file.file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Arquivo maior que 10 MB.")
    if not data:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")
    if not any(data.startswith(sig) for sig in MAGIC_BYTES[ext]):
        raise HTTPException(status_code=400, detail="O conteúdo do arquivo não corresponde ao tipo informado.")

    return file_path(save_file(db, data, file.content_type, folder))


def get_file(db: Session, file_id: UUID) -> StoredFile | None:
    return db.query(StoredFile).filter(StoredFile.id == file_id).first()


def get_file_by_path(db: Session, path: str) -> StoredFile | None:
    """Resolve um caminho /files/<id>.<ext> (como guardado no banco) para o arquivo."""
    match = FILE_PATH_RE.match(path or "")
    if not match:
        return None
    try:
        return get_file(db, UUID(match.group("id")))
    except ValueError:
        return None
