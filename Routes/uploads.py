from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session

from Core.database import get_db
from Core.deps import get_current_user
from Models.user import User
from Services.storage_service import EXTENSIONS, get_file, upload_file

router = APIRouter(tags=["Uploads"])


# Só o admin logado envia arquivos.
@router.post("/uploads/", status_code=201)
def upload(
    folder: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return {"url": upload_file(db, file, folder)}


# Público: é daqui que o site carrega a foto e os PDFs.
@router.get("/files/{file_name}")
def serve_file(file_name: str, db: Session = Depends(get_db)):
    file_id, _, ext = file_name.partition(".")
    try:
        stored = get_file(db, UUID(file_id))
    except ValueError:
        stored = None
    if not stored or EXTENSIONS.get(stored.content_type) != ext:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")

    return Response(
        content=stored.data,
        media_type=stored.content_type,
        headers={
            # Cada upload gera um id novo, então o conteúdo de uma URL nunca muda:
            # o navegador pode guardar pra sempre e não pede de novo ao banco.
            "Cache-Control": "public, max-age=31536000, immutable",
            "Content-Disposition": f'inline; filename="{file_name}"',
            "X-Content-Type-Options": "nosniff",
        },
    )
