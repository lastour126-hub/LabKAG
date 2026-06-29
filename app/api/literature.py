from fastapi import APIRouter

from app.adapters.kag_query_adapter import query_literature
from app.schemas.paper import QueryLiteratureRequest
from app.services.skill_orchestrator import success_response

router = APIRouter(prefix="/v1/literature", tags=["literature"])


@router.post("/query")
def query_literature_route(request: QueryLiteratureRequest):
    result = query_literature(request)
    evidence = result.pop("evidence", [])
    return success_response(data=result, project_id=request.project_id, evidence=evidence)
