from app.schemas.evidence import Evidence
from app.schemas.extraction import (
    ExtractedConclusion,
    ExtractedResult,
    PaperExtractionResult,
    PaperMetadata,
)


def test_paper_extraction_result_accepts_minimal_evidence_bound_payload():
    evidence = Evidence(
        evidence_id="ev_001",
        document_id="doc_001",
        chunk_id="chunk_001",
        page=1,
        section_title="Results",
        source_text="The material showed stable catalytic activity.",
    )

    extraction = PaperExtractionResult(
        paper=PaperMetadata(title="A Test Paper", authors=["Ada Lovelace"], year="2026"),
        results=[
            ExtractedResult(
                result_id="res_001",
                description="The material showed stable catalytic activity.",
                evidence=[evidence],
            )
        ],
        conclusions=[
            ExtractedConclusion(
                conclusion_id="con_001",
                description="The material is promising for catalysis.",
                evidence=[evidence],
            )
        ],
        evidence=[evidence],
        document_id="doc_001",
    )

    assert extraction.paper.title == "A Test Paper"
    assert extraction.results[0].evidence[0].chunk_id == "chunk_001"
    assert extraction.conclusions[0].evidence[0].page == 1
