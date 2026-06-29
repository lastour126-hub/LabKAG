from app.schemas.evidence import Evidence
from app.schemas.extraction import ExtractedConclusion, ExtractedResult, PaperExtractionResult
from app.services.evidence_binder import bind_required_evidence


def test_bind_required_evidence_marks_missing_result_and_conclusion_for_review():
    extraction = PaperExtractionResult(
        document_id="doc_001",
        results=[ExtractedResult(result_id="res_001", description="Missing result evidence")],
        conclusions=[
            ExtractedConclusion(conclusion_id="con_001", description="Missing conclusion evidence")
        ],
    )

    warnings = bind_required_evidence(extraction)

    assert extraction.results[0].needs_review is True
    assert extraction.conclusions[0].needs_review is True
    assert warnings == [
        "Result res_001 has no evidence and was marked needs_review.",
        "Conclusion con_001 has no evidence and was marked needs_review.",
    ]


def test_bind_required_evidence_keeps_evidence_bound_items_clean():
    evidence = Evidence(
        evidence_id="ev_001",
        document_id="doc_001",
        chunk_id="chunk_001",
        page=1,
        source_text="Evidence text",
    )
    extraction = PaperExtractionResult(
        document_id="doc_001",
        results=[ExtractedResult(result_id="res_001", description="Bound", evidence=[evidence])],
        conclusions=[
            ExtractedConclusion(conclusion_id="con_001", description="Bound", evidence=[evidence])
        ],
        evidence=[evidence],
    )

    warnings = bind_required_evidence(extraction)

    assert warnings == []
    assert extraction.results[0].needs_review is False
    assert extraction.conclusions[0].needs_review is False
