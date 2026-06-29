from pydantic import BaseModel, Field


class SkillMetadata(BaseModel):
    request_id: str
    project_id: str | None = None
    created_at: str
    extra: dict = Field(default_factory=dict)
