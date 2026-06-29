from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "LabKAG"
    app_version: str = "0.1.0"
    data_dir: Path = Path("data")
    upload_dir: Path = Path("data/uploads")
    parsed_dir: Path = Path("data/parsed")
    extraction_dir: Path = Path("data/extractions")
    mock_kag: bool = True


settings = Settings()
