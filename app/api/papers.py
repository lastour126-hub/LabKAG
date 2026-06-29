from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from app.schemas.errors import ErrorCode
from app.schemas.paper import ExtractPaperRequest, IngestPaperRequest
from app.services.skill_orchestrator import (
    error_response,
    extract_paper,
    ingest_paper,
    success_response,
)
from app.storage.file_store import UnsupportedFileTypeError, file_store

router = APIRouter(prefix="/v1/papers", tags=["papers"])


@router.post("/upload")
async def upload_paper(file: Annotated[UploadFile, File(...)]):
    content = await file.read()
    try:
        result = file_store.save_upload(file.filename or "paper.pdf", content)
    except UnsupportedFileTypeError as exc:
        raise error_response(400, ErrorCode.UNSUPPORTED_FILE_TYPE, str(exc)) from exc
    return success_response(data=result)


@router.post("/extract")
def extract_paper_route(request: ExtractPaperRequest):
    return extract_paper(request)


@router.post("/ingest")
def ingest_paper_route(request: IngestPaperRequest):
    return ingest_paper(request)


@router.get("/{paper_id}/knowledge")
def get_paper_knowledge(
    paper_id: str,
    project_id: str | None = None,
    include_evidence: bool = True,
):
    data = {
        "paper": {"paper_id": paper_id},
        "methods": [],
        "materials": [],
        "conditions": [],
        "metrics": [],
        "results": [],
        "conclusions": [],
        "relations": [],
    }
    if include_evidence:
        data["evidence"] = []
    return success_response(data=data, project_id=project_id)
