from scripts.verify_m8_neo4j_closed_loop import (
    M8_EVIDENCE_ID,
    M8_PAPER_ID,
    M8_QUERY,
    build_ingest_payload,
)


def test_m8_ingest_payload_is_neo4j_only_and_searchable():
    payload = build_ingest_payload()

    assert payload["project_id"] == "neo4j_only"
    assert payload["confirm"] is True
    extraction = payload["paper_extraction"]
    assert extraction["paper"]["paper_id"] == M8_PAPER_ID
    assert extraction["evidence"][0]["evidence_id"] == M8_EVIDENCE_ID
    assert M8_QUERY in extraction["evidence"][0]["source_text"]
    assert extraction["results"][0]["evidence"][0]["evidence_id"] == M8_EVIDENCE_ID
