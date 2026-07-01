from scripts.verify_m7_closed_loop import (
    M7_EVIDENCE_ID,
    M7_PAPER_ID,
    M7_QUERY,
    build_ingest_payload,
)


def test_m7_ingest_payload_is_scoped_and_searchable(monkeypatch):
    monkeypatch.setenv("OPENSPG_PROJECT_ID", "test_project")

    payload = build_ingest_payload()

    assert payload["project_id"] == "test_project"
    assert payload["confirm"] is True
    extraction = payload["paper_extraction"]
    assert extraction["paper"]["paper_id"] == M7_PAPER_ID
    assert extraction["evidence"][0]["evidence_id"] == M7_EVIDENCE_ID
    assert M7_QUERY in extraction["evidence"][0]["source_text"]
    assert extraction["results"][0]["evidence"][0]["evidence_id"] == M7_EVIDENCE_ID
