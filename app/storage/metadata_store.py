import json
from pathlib import Path
from typing import Any

from app.config import settings


class MetadataStore:
    def __init__(self, extraction_dir: Path | None = None) -> None:
        self.extraction_dir = extraction_dir or settings.extraction_dir

    def save_extraction(self, document_id: str, payload: dict[str, Any]) -> Path:
        self.extraction_dir.mkdir(parents=True, exist_ok=True)
        path = self.extraction_dir / f"{document_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load_extraction(self, document_id: str) -> dict[str, Any] | None:
        path = self.extraction_dir / f"{document_id}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))


metadata_store = MetadataStore()
