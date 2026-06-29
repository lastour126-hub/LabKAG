from pathlib import Path

import fitz
from fastapi.testclient import TestClient

from app.main import app


def _make_pdf(path: Path, text: str = "LabKAG API paper\nResults are evidence bound.") -> None:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    document.save(path)
    document.close()


def test_upload_accepts_pdf_and_rejects_non_pdf(tmp_path: Path):
    client = TestClient(app)
    pdf_path = tmp_path / "paper.pdf"
    _make_pdf(pdf_path)

    with pdf_path.open("rb") as file:
        response = client.post(
            "/v1/papers/upload",
            files={"file": ("paper.pdf", file, "application/pdf")},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["data"]["file_id"]
    assert body["data"]["file_name"] == "paper.pdf"

    response = client.post(
        "/v1/papers/upload",
        files={"file": ("paper.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["errors"][0]["code"] == "unsupported_file_type"


def test_extract_paper_returns_extraction_and_evidence(tmp_path: Path):
    client = TestClient(app)
    pdf_path = tmp_path / "paper.pdf"
    _make_pdf(pdf_path)

    with pdf_path.open("rb") as file:
        upload_response = client.post(
            "/v1/papers/upload",
            files={"file": ("paper.pdf", file, "application/pdf")},
        )
    file_id = upload_response.json()["data"]["file_id"]

    response = client.post("/v1/papers/extract", json={"file_id": file_id})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["data"]["paper_extraction"]["document_id"]
    assert body["evidence"]
    assert body["metadata"]["request_id"]


def test_mock_ingest_query_search_and_knowledge_routes():
    client = TestClient(app)
    paper_extraction = {
        "document_id": "doc_001",
        "paper": {"title": "A Test Paper"},
        "results": [
            {
                "result_id": "res_001",
                "description": "A result",
                "evidence": [
                    {
                        "evidence_id": "ev_001",
                        "document_id": "doc_001",
                        "chunk_id": "chunk_001",
                        "page": 1,
                        "source_text": "A result",
                    }
                ],
            }
        ],
        "conclusions": [],
        "evidence": [
            {
                "evidence_id": "ev_001",
                "document_id": "doc_001",
                "chunk_id": "chunk_001",
                "page": 1,
                "source_text": "A result",
            }
        ],
    }

    ingest = client.post(
        "/v1/papers/ingest",
        json={"project_id": "labkag_demo", "paper_extraction": paper_extraction, "confirm": True},
    )
    assert ingest.status_code == 200
    assert ingest.json()["data"]["entities_created"] >= 1

    query = client.post(
        "/v1/literature/query",
        json={"question": "What does this paper report?", "project_id": "labkag_demo"},
    )
    assert query.status_code == 200
    assert query.json()["data"]["answer"]
    assert query.json()["evidence"]

    search = client.post(
        "/v1/evidence/search",
        json={"query": "result", "project_id": "labkag_demo", "top_k": 5},
    )
    assert search.status_code == 200
    assert isinstance(search.json()["evidence"], list)

    knowledge = client.get("/v1/papers/paper_001/knowledge?project_id=labkag_demo")
    assert knowledge.status_code == 200
    assert "paper" in knowledge.json()["data"]
