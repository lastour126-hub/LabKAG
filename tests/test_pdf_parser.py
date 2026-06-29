from pathlib import Path

import fitz
import pytest

from app.services.pdf_parser import parse_pdf


def test_parse_pdf_extracts_text_pages(tmp_path: Path):
    pdf_path = tmp_path / "paper.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "LabKAG parser test")
    document.save(pdf_path)
    document.close()

    parsed = parse_pdf(pdf_path, document_id="doc_001")

    assert parsed.document_id == "doc_001"
    assert parsed.pages[0].page == 1
    assert "LabKAG parser test" in parsed.pages[0].text


def test_parse_pdf_raises_file_not_found_for_missing_path(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        parse_pdf(tmp_path / "missing.pdf", document_id="doc_missing")
