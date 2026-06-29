from app.schemas.extraction import PaperExtractionResult


def map_extraction_to_graph(extraction: PaperExtractionResult) -> dict:
    entities: list[dict] = []
    relations: list[dict] = []

    paper_id = extraction.paper.paper_id or f"paper_{extraction.document_id}"
    entities.append(
        {
            "id": paper_id,
            "type": "Paper",
            "properties": extraction.paper.model_dump(),
        }
    )

    for method in extraction.methods:
        entity_id = method.method_id
        entities.append({"id": entity_id, "type": "Method", "properties": method.model_dump()})
        relations.append({"source": paper_id, "relation": "proposes", "target": entity_id})

    for material in extraction.materials:
        entity_id = material.material_id
        entities.append({"id": entity_id, "type": "Material", "properties": material.model_dump()})
        relations.append({"source": paper_id, "relation": "uses", "target": entity_id})

    for result in extraction.results:
        entity_id = result.result_id
        entities.append({"id": entity_id, "type": "Result", "properties": result.model_dump()})
        relations.append({"source": paper_id, "relation": "reports", "target": entity_id})

    for conclusion in extraction.conclusions:
        entity_id = conclusion.conclusion_id
        entities.append(
            {"id": entity_id, "type": "Conclusion", "properties": conclusion.model_dump()}
        )
        relations.append({"source": paper_id, "relation": "draws_conclusion", "target": entity_id})

    for evidence in extraction.evidence:
        entities.append(
            {"id": evidence.evidence_id, "type": "Evidence", "properties": evidence.model_dump()}
        )

    return {"entities": entities, "relations": relations}
