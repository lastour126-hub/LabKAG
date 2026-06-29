from pathlib import Path

import fitz

from app.schemas.document import DocumentPage, ParsedDocument


def parse_pdf(path: Path | str, document_id: str) -> ParsedDocument:
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    pages: list[DocumentPage] = []
    with fitz.open(pdf_path) as document:
        for index, page in enumerate(document, start=1):
            pages.append(DocumentPage(page=index, text=page.get_text("text").strip()))

    return ParsedDocument(document_id=document_id, file_name=pdf_path.name, pages=pages)
