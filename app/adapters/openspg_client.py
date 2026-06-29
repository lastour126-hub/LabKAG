class OpenSPGClient:
    def write_graph(self, graph_payload: dict, confirm: bool = False) -> dict:
        return {
            "paper_id": "paper_001",
            "entities_created": len(graph_payload.get("entities", [])) if confirm else 0,
            "relations_created": len(graph_payload.get("relations", [])) if confirm else 0,
            "evidence_created": len(
                [
                    entity
                    for entity in graph_payload.get("entities", [])
                    if entity.get("type") == "Evidence"
                ]
            )
            if confirm
            else 0,
            "dry_run": not confirm,
        }


openspg_client = OpenSPGClient()
