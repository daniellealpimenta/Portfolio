from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, deferred
from Models.base import BaseORMModel


class StoredFile(BaseORMModel):
    """Arquivo enviado pelo admin (foto, currículos), guardado no próprio Postgres.

    O site referencia o arquivo pelo caminho relativo /files/<id>.<ext>; o
    frontend completa com o endereço da API na hora de exibir.
    """
    __tablename__ = "stored_file"

    folder: Mapped[str] = mapped_column(nullable=False)
    content_type: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)
    # deferred: listar/consultar metadados não carrega os bytes
    data: Mapped[bytes] = deferred(mapped_column(LargeBinary, nullable=False))
