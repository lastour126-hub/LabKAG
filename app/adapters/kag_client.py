from app.schemas.evidence import Evidence


class KAGClient:
    def query(self, question: str, top_k: int = 5) -> dict:
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

    def search_evidence(self, query: str, top_k: int = 10) -> list[Evidence]:
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


kag_client = KAGClient()
