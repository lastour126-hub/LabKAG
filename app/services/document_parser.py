from pathlib import Path

from app.schemas.document import ParsedDocument
from app.services.pdf_parser import parse_pdf


def parse_document(path: Path, document_id: str) -> ParsedDocument:
    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF documents are supported in v0.1.")
    return parse_pdf(path, document_id)
