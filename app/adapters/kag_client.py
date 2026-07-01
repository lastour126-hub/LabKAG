from typing import Any

from app.adapters.neo4j_query_store import Neo4jQueryStore
from app.config import settings
from app.schemas.evidence import Evidence


class KAGClient:
    def __init__(self, mock: bool | None = None, query_store: Any | None = None) -> None:
        self.mock = settings.mock_kag if mock is None else mock
        self.query_store = query_store

    def query(
        self,
        question: str,
        project_id: str | None = None,
        paper_id: str | None = None,
        top_k: int = 5,
    ) -> dict:
        if not self.mock:
            results = self._query_store().search_evidence(
                question,
                project_id=project_id,
                paper_id=paper_id,
                top_k=top_k,
            )
            return self._answer_from_evidence(results)

        evidence = Evidence(
            evidence_id="ev_mock_001",
            document_id="doc_mock",
            paper_id="paper_001",
            chunk_id="chunk_mock_001",
            page=1,
            section_title="Mock Evidence",
            source_text="Mock KAG evidence for the requested literature question.",
        )
        return {
            "answer": f"Mock answer for: {question}",
            "related_entities": [],
            "reasoning_path": [],
            "confidence": "medium",
            "evidence": [evidence],
        }

    def search_evidence(
        self,
        query: str,
        project_id: str | None = None,
        paper_id: str | None = None,
        top_k: int = 10,
    ) -> list[Evidence]:
        if not self.mock:
            return [
                result.evidence
                for result in self._query_store().search_evidence(
                    query,
                    project_id=project_id,
                    paper_id=paper_id,
                    top_k=top_k,
                )
            ]

        return [
            Evidence(
                evidence_id="ev_mock_001",
                document_id="doc_mock",
                paper_id="paper_001",
                chunk_id="chunk_mock_001",
                page=1,
                section_title="Mock Evidence",
                source_text=f"Mock evidence matched query: {query}",
            )
        ][:top_k]

    def _query_store(self) -> Any:
        if self.query_store is not None:
            return self.query_store
        if settings.openspg_write_backend != "neo4j":
            raise RuntimeError("Real KAG query requires OPENSPG_WRITE_BACKEND=neo4j for v0.1.")
        if not settings.openspg_neo4j_password:
            raise RuntimeError("OPENSPG_NEO4J_PASSWORD is required for real KAG query.")
        self.query_store = Neo4jQueryStore(
            uri=settings.openspg_neo4j_uri,
            user=settings.openspg_neo4j_user,
            password=settings.openspg_neo4j_password,
            database=settings.openspg_neo4j_database,
        )
        return self.query_store

    @staticmethod
    def _answer_from_evidence(results: list[Any]) -> dict:
        if not results:
            return {
                "answer": "No matching evidence found.",
                "related_entities": [],
                "reasoning_path": [],
                "confidence": "low",
                "evidence": [],
            }

        evidence = [result.evidence for result in results]
        related_entities = []
        reasoning_path = []
        for result in results:
            paper = result.paper or {}
            paper_id = paper.get("id") or result.evidence.paper_id
            if paper_id:
                related_entities.append(
                    {"id": paper_id, "type": "Paper", "title": paper.get("title", "")}
                )
                reasoning_path.append(paper_id)
            reasoning_path.append(result.evidence.evidence_id)

        return {
            "answer": " ".join(item.source_text for item in evidence if item.source_text),
            "related_entities": related_entities,
            "reasoning_path": reasoning_path,
            "confidence": "medium",
            "evidence": evidence,
        }


kag_client = KAGClient()
