from typing import Any

from app.adapters.graph_store_factory import GraphStoreFactoryError, build_graph_store
from app.config import settings


class GraphWriteError(RuntimeError):
    pass


class GraphClient:
    def __init__(self, mock: bool | None = None, graph_store: Any | None = None) -> None:
        self.mock = settings.mock_kag if mock is None else mock
        self.graph_store = graph_store

    def write_graph(
        self,
        graph_payload: dict,
        confirm: bool = False,
        project_id: str | None = None,
    ) -> dict:
        if self.mock or not confirm:
            return self._mock_result(graph_payload, confirm=confirm)

        try:
            payload = self._graph_store().write_graph(graph_payload, project_id=project_id)
        except GraphStoreFactoryError as exc:
            raise GraphWriteError(str(exc)) from exc
        return self._write_result(graph_payload, payload)

    def _graph_store(self) -> Any:
        if self.graph_store is None:
            self.graph_store = build_graph_store(settings)
        return self.graph_store

    @staticmethod
    def _write_result(graph_payload: dict, payload: dict) -> dict:
        return {
            "paper_id": payload.get("paper_id")
            or GraphClient._paper_id_from_payload(graph_payload),
            "entities_created": payload.get("entities_created", 0),
            "relations_created": payload.get("relations_created", 0),
            "evidence_created": payload.get("evidence_created", 0),
            "dry_run": False,
            "mock": False,
        }

    @staticmethod
    def _paper_id_from_payload(graph_payload: dict) -> str:
        for entity in graph_payload.get("entities", []):
            if entity.get("type") == "Paper":
                return entity.get("id", "paper_001")
        return "paper_001"

    def _mock_result(self, graph_payload: dict, confirm: bool = False) -> dict:
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
            "mock": self.mock,
        }


graph_client = GraphClient()
