from app.schemas.extraction import PaperExtractionResult


def bind_required_evidence(extraction: PaperExtractionResult) -> list[str]:
    warnings: list[str] = []

    for result in extraction.results:
        if not result.evidence:
            result.needs_review = True
            result_id = result.result_id or "unknown"
            warnings.append(f"Result {result_id} has no evidence and was marked needs_review.")

    for conclusion in extraction.conclusions:
        if not conclusion.evidence:
            conclusion.needs_review = True
            conclusion_id = conclusion.conclusion_id or "unknown"
            warnings.append(
                f"Conclusion {conclusion_id} has no evidence and was marked needs_review."
            )

    return warnings
