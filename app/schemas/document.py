from pydantic import BaseModel, Field


class DocumentPage(BaseModel):
    page: int
    text: str = ""


class DocumentChunk(BaseModel):
    document_id: str
    chunk_id: str
    page: int
    text: str
    section_title: str | None = None


class ParsedDocument(BaseModel):
    document_id: str
    file_name: str = ""
    title: str = ""
    pages: list[DocumentPage] = Field(default_factory=list)
    chunks: list[DocumentChunk] = Field(default_factory=list)
