from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.common import SkillMetadata
from app.schemas.errors import SkillError
from app.schemas.evidence import Evidence

SkillStatus = Literal["success", "partial_success", "failed", "needs_review"]


class SkillResponse(BaseModel):
    status: SkillStatus
    data: dict[str, Any] = Field(default_factory=dict)
    evidence: list[Evidence | dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    errors: list[SkillError] = Field(default_factory=list)
    metadata: SkillMetadata
