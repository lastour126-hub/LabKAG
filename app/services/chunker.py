from app.schemas.document import DocumentChunk, DocumentPage


def _section_title(text: str) -> str | None:
    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    return first_line[:80] if first_line else None


def chunk_pages(
    document_id: str,
    pages: list[DocumentPage],
    max_chars: int = 1800,
) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    counter = 1
    for page in pages:
        text = page.text.strip()
        if not text:
            continue
        for start in range(0, len(text), max_chars):
            chunk_text = text[start : start + max_chars].strip()
            if not chunk_text:
                continue
            chunks.append(
                DocumentChunk(
                    document_id=document_id,
                    chunk_id=f"{document_id}_chunk_{counter:03d}",
                    page=page.page,
                    section_title=_section_title(chunk_text),
                    text=chunk_text,
                )
            )
            counter += 1
    return chunks
