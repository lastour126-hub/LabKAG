from fastapi import APIRouter

from app.adapters.kag_query_adapter import search_evidence
from app.schemas.paper import SearchEvidenceRequest
from app.services.skill_orchestrator import success_response

router = APIRouter(prefix="/v1/evidence", tags=["evidence"])


@router.post("/search")
def search_evidence_route(request: SearchEvidenceRequest):
    evidence = search_evidence(request)
    return success_response(
        data={"matched_entities": []},
        project_id=request.project_id,
        evidence=evidence,
    )
