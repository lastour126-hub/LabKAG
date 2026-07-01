"""Run the LabKAG M7 local closed-loop verification.

This script uses the FastAPI app in-process and writes to the configured local
OpenSPG Neo4j graph store. It is intended for a reproducible handoff check.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

M7_PROJECT_ID = "1"
M7_PAPER_ID = "m7_closed_loop_paper_001"
M7_EVIDENCE_ID = "m7_closed_loop_ev_001"
M7_QUERY = "M7 verification marker 2026"
M7_EVIDENCE_TEXT = (
    "M7 verification marker 2026: catalyst A reached 95% conversion in the "
    "literature-only closed loop."
)


def configure_environment() -> None:
    defaults = {
        "MOCK_KAG": "false",
        "OPENSPG_BASE_URL": "http://127.0.0.1:8887",
        "OPENSPG_ACCOUNT": "openspg",
        "OPENSPG_PASSWORD": "openspg123",
        "OPENSPG_PROJECT_ID": M7_PROJECT_ID,
        "OPENSPG_PROJECT_NAME": "LabKAG",
        "OPENSPG_NAMESPACE": "LabKAG",
        "OPENSPG_WRITE_BACKEND": "neo4j",
        "OPENSPG_NEO4J_URI": "neo4j://127.0.0.1:7687",
        "OPENSPG_NEO4J_USER": "neo4j",
        "OPENSPG_NEO4J_PASSWORD": "openspgneo4j",
        "OPENSPG_NEO4J_DATABASE": "neo4j",
    }
    for key, value in defaults.items():
        os.environ.setdefault(key, value)


def build_ingest_payload() -> dict[str, Any]:
    evidence = {
        "evidence_id": M7_EVIDENCE_ID,
        "document_id": "m7_closed_loop_doc_001",
        "chunk_id": "m7_closed_loop_chunk_001",
        "page": 1,
        "section_title": "Results",
        "source_text": M7_EVIDENCE_TEXT,
    }
    return {
        "project_id": os.environ.get("OPENSPG_PROJECT_ID", M7_PROJECT_ID),
        "confirm": True,
        "paper_extraction": {
            "document_id": "m7_closed_loop_doc_001",
            "paper": {
                "paper_id": M7_PAPER_ID,
                "title": "M7 Closed Loop Verification Paper",
                "authors": ["LabKAG"],
                "year": "2026",
                "abstract": "Minimal literature-only verification payload.",
            },
            "methods": [
                {
                    "method_id": "m7_closed_loop_method_001",
                    "name": "Local verification",
                    "description": "FastAPI to Neo4j closed-loop verification.",
                    "method_type": "validation",
                    "evidence": [evidence],
                }
            ],
            "results": [
                {
                    "result_id": "m7_closed_loop_result_001",
                    "description": "Catalyst A reached 95% conversion.",
                    "value": "95",
                    "unit": "%",
                    "result_type": "conversion",
                    "evidence": [evidence],
                }
            ],
            "evidence": [evidence],
        },
    }


def require_success(response: Any, step: str) -> dict[str, Any]:
    if response.status_code != 200:
        raise RuntimeError(f"{step} failed with HTTP {response.status_code}: {response.text}")
    body = response.json()
    if body.get("status") != "success":
        raise RuntimeError(f"{step} failed: {body}")
    print(f"PASS {step}")
    return body


def main() -> int:
    configure_environment()

    try:
        from fastapi.testclient import TestClient

        from app.adapters.openspg_client import OpenSPGClient
        from app.main import app

        client = TestClient(app)

        health = client.get("/health")
        if health.status_code != 200:
            raise RuntimeError(f"health failed with HTTP {health.status_code}: {health.text}")
        print("PASS health")

        schema = OpenSPGClient(mock=False).apply_literature_schema()
        print(f"PASS schema entity_types={len(schema['entity_types'])}")

        ingest = require_success(
            client.post("/v1/papers/ingest", json=build_ingest_payload()),
            "ingest",
        )
        if ingest["data"].get("mock") is not False:
            raise RuntimeError(f"ingest did not use real backend: {ingest['data']}")
        if ingest["data"].get("evidence_created", 0) < 1:
            raise RuntimeError(f"ingest created no evidence: {ingest['data']}")

        search = require_success(
            client.post(
                "/v1/evidence/search",
                json={
                    "query": M7_QUERY,
                    "project_id": os.environ["OPENSPG_PROJECT_ID"],
                    "paper_id": M7_PAPER_ID,
                    "top_k": 5,
                },
            ),
            "evidence_search",
        )
        evidence_ids = [item["evidence_id"] for item in search["evidence"]]
        if evidence_ids != [M7_EVIDENCE_ID]:
            raise RuntimeError(f"unexpected evidence ids: {evidence_ids}")

        query = require_success(
            client.post(
                "/v1/literature/query",
                json={
                    "question": M7_QUERY,
                    "project_id": os.environ["OPENSPG_PROJECT_ID"],
                    "paper_id": M7_PAPER_ID,
                    "top_k": 5,
                },
            ),
            "literature_query",
        )
        if M7_EVIDENCE_TEXT not in query["data"].get("answer", ""):
            raise RuntimeError(f"answer does not cite expected evidence text: {query['data']}")

        print("M7 closed loop verification passed.")
        return 0
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
