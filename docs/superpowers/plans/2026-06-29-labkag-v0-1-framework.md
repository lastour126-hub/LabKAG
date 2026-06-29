# LabKAG v0.1 Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first runnable LabKAG v0.1 FastAPI Skill Server framework with a stable API contract and mock OpenSPG/KAG boundaries.

**Architecture:** The first version separates HTTP routes, Pydantic schemas, service orchestration, local storage, document processing, evidence binding, and OpenSPG/KAG adapters. OpenSPG/KAG and LLM extraction are represented by replaceable mock adapters first, so the API contract and local processing loop can be verified before integrating external systems.

**Tech Stack:** Python 3.10, FastAPI, Pydantic v2, Uvicorn, pytest, PyMuPDF, python-dotenv, ruff.

---

## Scope

This plan builds the first implementation framework for LabKAG v0.1:

```text
health
-> upload PDF
-> parse PDF
-> chunk text
-> mock paper extraction
-> evidence binding
-> mock ingest
-> mock literature query
-> mock evidence search
```

This plan intentionally does not implement real OpenSPG writes, real KAG reasoning, real LLM extraction, authentication, OCR, database persistence, frontend UI, or complex table/image parsing.

## File Structure

```text
app/
  main.py                         FastAPI app factory and router registration
  config.py                       Runtime settings and local data paths
  api/
    health.py                     Health endpoint
    papers.py                     Upload, extract, ingest, and paper knowledge routes
    literature.py                 Literature query route
    evidence.py                   Evidence search route
  schemas/
    response.py                   Unified SkillResponse schema
    errors.py                     Error code schema
    document.py                   Parsed document, page, and chunk schemas
    evidence.py                   Evidence schema
    extraction.py                 PaperExtractionResult and extracted object schemas
    paper.py                      Paper request and response schemas
    common.py                     Shared primitive aliases and metadata schemas
  services/
    pdf_parser.py                 Text PDF parsing through PyMuPDF
    chunker.py                    Page text to evidence-ready chunks
    paper_extractor.py            First mock extractor
    evidence_binder.py            Evidence validation and binding
    skill_orchestrator.py         Use-case orchestration
    document_parser.py            File-type dispatch boundary
  adapters/
    openspg_mapper.py             PaperExtractionResult to graph payload mapping
    openspg_client.py             Mock OpenSPG write client
    kag_client.py                 Mock KAG query client
    kag_query_adapter.py          Query and evidence-search adapter
  storage/
    file_store.py                 Upload and file lookup
    metadata_store.py             Local JSON metadata persistence
  utils/
    ids.py                        ID generation helpers
    time.py                       Timestamp helpers
    logging.py                    Logging setup
examples/
  upload_paper.py                 Example upload call
  extract_paper.py                Example extraction call
  ingest_paper.py                 Example ingest call
  query_literature.py             Example literature query call
  search_evidence.py              Example evidence search call
tests/
  test_health.py
  test_pdf_parser.py
  test_chunker.py
  test_extraction_schema.py
  test_evidence_binder.py
  test_skill_api.py
```

## Task 1: Project Configuration

**Files:**
- Modify: `pyproject.toml`
- Modify: `requirements.txt`
- Modify: `.env.example`
- Modify: `app/config.py`

- [ ] **Step 1: Write dependency files**

Set `requirements.txt` to:

```text
fastapi
uvicorn[standard]
pydantic
pydantic-settings
python-dotenv
PyMuPDF
pytest
ruff
```

Set `pyproject.toml` to define Python 3.10, pytest, and ruff basics:

```toml
[project]
name = "labkag"
version = "0.1.0"
requires-python = ">=3.10,<3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

- [ ] **Step 2: Add environment example**

Set `.env.example` to:

```text
APP_NAME=LabKAG
APP_VERSION=0.1.0
DATA_DIR=data
UPLOAD_DIR=data/uploads
PARSED_DIR=data/parsed
EXTRACTION_DIR=data/extractions
MOCK_KAG=true
```

- [ ] **Step 3: Implement settings**

Implement `app/config.py` with a Pydantic settings object that exposes those fields and creates no side effects on import.

- [ ] **Step 4: Verify config imports**

Run:

```powershell
python -c "from app.config import settings; print(settings.app_name, settings.mock_kag)"
```

Expected output includes:

```text
LabKAG True
```

## Task 2: Unified Schemas

**Files:**
- Modify: `app/schemas/response.py`
- Modify: `app/schemas/errors.py`
- Modify: `app/schemas/document.py`
- Modify: `app/schemas/evidence.py`
- Modify: `app/schemas/extraction.py`
- Modify: `app/schemas/paper.py`
- Modify: `app/schemas/common.py`
- Test: `tests/test_extraction_schema.py`

- [ ] **Step 1: Add schema tests**

Create tests that instantiate a minimal `PaperExtractionResult` with one result, one conclusion, and one evidence item.

- [ ] **Step 2: Implement schemas**

Use Pydantic models for:

```text
SkillResponse
SkillMetadata
SkillError
DocumentPage
DocumentChunk
ParsedDocument
Evidence
PaperMetadata
ExtractedMethod
ExtractedMaterial
ExtractedCondition
ExtractedMetric
ExtractedResult
ExtractedConclusion
PaperExtractionResult
```

- [ ] **Step 3: Run schema tests**

Run:

```powershell
pytest tests/test_extraction_schema.py -v
```

Expected: all tests pass.

## Task 3: Health API

**Files:**
- Modify: `app/main.py`
- Modify: `app/api/health.py`
- Test: `tests/test_health.py`

- [ ] **Step 1: Write health test**

Assert `GET /health` returns HTTP 200 and a unified response with `status="success"`.

- [ ] **Step 2: Implement FastAPI app and route**

Register `app/api/health.py` in `app/main.py`.

- [ ] **Step 3: Run health test**

Run:

```powershell
pytest tests/test_health.py -v
```

Expected: all tests pass.

## Task 4: Local File Storage and Upload API

**Files:**
- Modify: `app/storage/file_store.py`
- Modify: `app/api/papers.py`
- Modify: `app/main.py`
- Test: `tests/test_skill_api.py`

- [ ] **Step 1: Write upload API test**

Test that a small fake PDF-like file upload is accepted only when the filename ends with `.pdf`, saved under `data/uploads`, and returns a `file_id`.

- [ ] **Step 2: Implement FileStore**

Implement methods for saving upload bytes, resolving a `file_id`, and rejecting unsupported suffixes.

- [ ] **Step 3: Implement `POST /v1/papers/upload`**

Return unified `SkillResponse` containing `file_id`, `file_name`, and `stored_path`.

- [ ] **Step 4: Run upload tests**

Run:

```powershell
pytest tests/test_skill_api.py -v
```

Expected: upload tests pass.

## Task 5: PDF Parser and Chunker

**Files:**
- Modify: `app/services/pdf_parser.py`
- Modify: `app/services/chunker.py`
- Test: `tests/test_pdf_parser.py`
- Test: `tests/test_chunker.py`

- [ ] **Step 1: Write parser and chunker tests**

Test parser behavior for missing files and chunker behavior for page/chunk ID retention.

- [ ] **Step 2: Implement PDF parser**

Use PyMuPDF to extract text from text-based PDFs into `DocumentPage` objects.

- [ ] **Step 3: Implement chunker**

Generate `DocumentChunk` objects with:

```text
document_id
chunk_id
page
section_title
text
```

- [ ] **Step 4: Run parser and chunker tests**

Run:

```powershell
pytest tests/test_pdf_parser.py tests/test_chunker.py -v
```

Expected: all tests pass.

## Task 6: Mock Paper Extraction and Evidence Binding

**Files:**
- Modify: `app/services/paper_extractor.py`
- Modify: `app/services/evidence_binder.py`
- Test: `tests/test_evidence_binder.py`
- Test: `tests/test_extraction_schema.py`

- [ ] **Step 1: Write evidence binder tests**

Test that results and conclusions without evidence are marked for review or receive a warning.

- [ ] **Step 2: Implement mock extractor**

Use parsed chunks to produce a minimal `PaperExtractionResult`. Use the first non-empty page/chunk as evidence for mock result and conclusion.

- [ ] **Step 3: Implement evidence binder**

Validate that all result and conclusion objects have evidence. Return warnings when evidence is missing.

- [ ] **Step 4: Run extraction and evidence tests**

Run:

```powershell
pytest tests/test_extraction_schema.py tests/test_evidence_binder.py -v
```

Expected: all tests pass.

## Task 7: Extract Paper Orchestration

**Files:**
- Modify: `app/services/skill_orchestrator.py`
- Modify: `app/api/papers.py`
- Test: `tests/test_skill_api.py`

- [ ] **Step 1: Write extract endpoint test**

Test `POST /v1/papers/extract` with a known `file_id` returns:

```text
status=success
data.paper_extraction
evidence array
metadata.request_id
```

- [ ] **Step 2: Implement orchestrator extraction flow**

Wire:

```text
file_store
-> pdf_parser
-> chunker
-> paper_extractor
-> evidence_binder
-> SkillResponse
```

- [ ] **Step 3: Run skill API tests**

Run:

```powershell
pytest tests/test_skill_api.py -v
```

Expected: upload and extraction tests pass.

## Task 8: Mock OpenSPG/KAG Adapters

**Files:**
- Modify: `app/adapters/openspg_mapper.py`
- Modify: `app/adapters/openspg_client.py`
- Modify: `app/adapters/kag_client.py`
- Modify: `app/adapters/kag_query_adapter.py`
- Modify: `app/api/papers.py`
- Modify: `app/api/literature.py`
- Modify: `app/api/evidence.py`
- Test: `tests/test_skill_api.py`

- [ ] **Step 1: Write adapter endpoint tests**

Test:

```text
POST /v1/papers/ingest
POST /v1/literature/query
POST /v1/evidence/search
GET /v1/papers/{paper_id}/knowledge
```

- [ ] **Step 2: Implement graph mapper**

Map methods, materials, results, conclusions, and evidence into entity/relation dictionaries.

- [ ] **Step 3: Implement mock clients**

Return deterministic counts and evidence-aware mock answers.

- [ ] **Step 4: Register routes**

Expose all v0.1 API routes through FastAPI.

- [ ] **Step 5: Run skill API tests**

Run:

```powershell
pytest tests/test_skill_api.py -v
```

Expected: all API tests pass.

## Task 9: Examples and Basic Docs

**Files:**
- Modify: `examples/upload_paper.py`
- Modify: `examples/extract_paper.py`
- Modify: `examples/ingest_paper.py`
- Modify: `examples/query_literature.py`
- Modify: `examples/search_evidence.py`
- Modify: `README.md`
- Modify: `docs/API.md`
- Modify: `docs/LabKAG_Literature_Schema_v0.1.md`

- [ ] **Step 1: Add example scripts**

Each example should call one endpoint with `requests` or clearly show the JSON body for curl-compatible use.

- [ ] **Step 2: Add README quickstart**

Include:

```text
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest -v
```

- [ ] **Step 3: Add API contract summary**

Document the v0.1 routes and unified response shape.

## Task 10: Final Verification

**Files:**
- No new files.

- [ ] **Step 1: Run tests**

Run:

```powershell
pytest -v
```

Expected: all tests pass.

- [ ] **Step 2: Run lint**

Run:

```powershell
ruff check .
```

Expected: no lint errors.

- [ ] **Step 3: Run server smoke check**

Run:

```powershell
uvicorn app.main:app --reload
```

Then check:

```powershell
curl http://127.0.0.1:8000/health
```

Expected: JSON response with `status` equal to `success`.

## Execution Notes

Use small commits after each task. Do not integrate real OpenSPG/KAG or real LLM extraction in this first framework pass. Keep adapter interfaces stable so the second implementation pass can replace mocks without changing API routes.
