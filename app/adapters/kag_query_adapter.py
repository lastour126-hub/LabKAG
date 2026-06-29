from app.adapters.kag_client import kag_client
from app.schemas.paper import QueryLiteratureRequest, SearchEvidenceRequest


def query_literature(request: QueryLiteratureRequest) -> dict:
    return kag_client.query(request.question, top_k=request.top_k)


def search_evidence(request: SearchEvidenceRequest):
    return kag_client.search_evidence(request.query, top_k=request.top_k)
