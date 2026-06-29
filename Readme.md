# LabKAG

LabKAG v0.1 is a Skill-first FastAPI service for literature knowledge extraction,
evidence binding, and mock OpenSPG/KAG integration.

## Quickstart

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/init_storage.py
uvicorn app.main:app --reload
```

Run tests:

```powershell
py -3.10 -m pytest -v
py -3.10 -m ruff check .
```

## v0.1 Scope

Implemented in this first framework pass:

- Unified SkillResponse contract
- PDF upload
- Text PDF parsing through PyMuPDF
- Evidence-ready chunking
- Mock paper extraction
- Evidence binding validation
- Mock OpenSPG ingest
- Mock KAG literature query and evidence search

Not implemented yet:

- Real LLM extraction
- Real OpenSPG writes
- Real KAG reasoning
- OCR
- Authentication
- Frontend UI
