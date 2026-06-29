from app.schemas.document import DocumentPage
from app.services.chunker import chunk_pages


def test_chunk_pages_retains_document_id_page_and_chunk_id():
    pages = [
        DocumentPage(page=1, text="Abstract\nThis is the first page."),
        DocumentPage(page=2, text="Results\nThis is the second page."),
    ]

    chunks = chunk_pages("doc_001", pages, max_chars=100)

    assert [chunk.document_id for chunk in chunks] == ["doc_001", "doc_001"]
    assert [chunk.page for chunk in chunks] == [1, 2]
    assert [chunk.chunk_id for chunk in chunks] == ["doc_001_chunk_001", "doc_001_chunk_002"]
    assert chunks[0].section_title == "Abstract"
