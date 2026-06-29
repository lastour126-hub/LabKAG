from pathlib import Path

from app.config import settings
from app.utils.ids import new_id


class UnsupportedFileTypeError(ValueError):
    pass


class FileStore:
    def __init__(self, upload_dir: Path | None = None) -> None:
        self.upload_dir = upload_dir or settings.upload_dir

    def save_upload(self, file_name: str, content: bytes) -> dict[str, str]:
        if not file_name.lower().endswith(".pdf"):
            raise UnsupportedFileTypeError("Only PDF files are supported.")

        self.upload_dir.mkdir(parents=True, exist_ok=True)
        file_id = new_id("file")
        stored_name = f"{file_id}.pdf"
        stored_path = self.upload_dir / stored_name
        stored_path.write_bytes(content)

        return {
            "file_id": file_id,
            "file_name": file_name,
            "stored_path": str(stored_path),
        }

    def resolve(self, file_id: str) -> Path:
        path = self.upload_dir / f"{file_id}.pdf"
        if not path.exists():
            raise FileNotFoundError(f"File {file_id} was not found.")
        return path


file_store = FileStore()
