from fastapi import APIRouter

from app.adapters.kag_query_adapter import search_evidence
from app.schemas.errors import ErrorCode
from app.schemas.paper import SearchEvidenceRequest
from app.services.skill_orchestrator import error_response, success_response

router = APIRouter(prefix="/v1/evidence", tags=["evidence"])


@router.post("/search")
def search_evidence_route(request: SearchEvidenceRequest):
    try:
        evidence = search_evidence(request)
    except RuntimeError as exc:
        raise error_response(502, ErrorCode.KAG_QUERY_FAILED, str(exc)) from exc
    return success_response(
        data={"matched_entities": []},
        project_id=request.project_id,
        evidence=evidence,
    )
