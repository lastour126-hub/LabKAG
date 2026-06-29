from app.schemas.document import DocumentChunk, ParsedDocument
from app.schemas.evidence import Evidence
from app.schemas.extraction import (
    ExtractedConclusion,
    ExtractedMethod,
    ExtractedResult,
    PaperExtractionResult,
    PaperMetadata,
)
from app.utils.ids import new_id
from app.utils.time import utc_now_iso


def _first_evidence(chunks: list[DocumentChunk]) -> Evidence | None:
    for chunk in chunks:
        if chunk.text.strip():
            source_text = chunk.text.strip()
            return Evidence(
                evidence_id=new_id("ev"),
                document_id=chunk.document_id,
                chunk_id=chunk.chunk_id,
                page=chunk.page,
                section_title=chunk.section_title,
                source_text=source_text[:500],
            )
    return None


def extract_paper_mock(document: ParsedDocument) -> PaperExtractionResult:
    evidence = _first_evidence(document.chunks)
    first_text = evidence.source_text if evidence else ""
    title = document.title or first_text.splitlines()[0][:120] if first_text else ""

    evidence_list = [evidence] if evidence else []
    return PaperExtractionResult(
        document_id=document.document_id,
        paper=PaperMetadata(
            paper_id=new_id("paper"),
            title=title,
            document_id=document.document_id,
        ),
        methods=[
            ExtractedMethod(
                method_id=new_id("method"),
                name="mock_method",
                description="Mock method extracted from parsed document text.",
                evidence=evidence_list,
                inferred=True,
            )
        ]
        if evidence
        else [],
        results=[
            ExtractedResult(
                result_id=new_id("res"),
                description="Mock result extracted from parsed document text.",
                evidence=evidence_list,
                inferred=True,
            )
        ]
        if evidence
        else [],
        conclusions=[
            ExtractedConclusion(
                conclusion_id=new_id("con"),
                description="Mock conclusion extracted from parsed document text.",
                evidence=evidence_list,
                inferred=True,
            )
        ]
        if evidence
        else [],
        evidence=evidence_list,
        created_at=utc_now_iso(),
    )
