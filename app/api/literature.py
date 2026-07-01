from fastapi import APIRouter

from app.adapters.kag_query_adapter import query_literature
from app.schemas.errors import ErrorCode
from app.schemas.paper import QueryLiteratureRequest
from app.services.skill_orchestrator import error_response, success_response

router = APIRouter(prefix="/v1/literature", tags=["literature"])


@router.post("/query")
def query_literature_route(request: QueryLiteratureRequest):
    try:
        result = query_literature(request)
    except RuntimeError as exc:
        raise error_response(502, ErrorCode.KAG_QUERY_FAILED, str(exc)) from exc
    evidence = result.pop("evidence", [])
    return success_response(data=result, project_id=request.project_id, evidence=evidence)
