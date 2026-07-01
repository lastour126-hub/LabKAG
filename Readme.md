# LabKAG

LabKAG v0.1 is a Skill-first FastAPI service for literature knowledge extraction,
evidence binding, and configurable OpenSPG/KAG integration.

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

Run the local closed-loop verification after the OpenSPG compose stack is up:

```powershell
py -3.10 scripts\verify_m7_closed_loop.py
```

## v0.1 Scope

Implemented in this first framework pass:

- Unified SkillResponse contract
- PDF upload
- Text PDF parsing through PyMuPDF
- Evidence-ready chunking
- Mock paper extraction
- OpenAI-compatible LLM extraction path for M3
- Evidence binding validation
- Configurable OpenSPG/KAG adapter for M5
- Literature schema application through OpenSPG KGDSL
- Real local graph writes through the OpenSPG Neo4j backend
- Evidence search and literature query over Neo4j for M6

Not implemented yet:

- OCR
- Authentication
- Frontend UI
- OpenSPG official data-write API integration
- OpenSPG built-in conversation system integration

## LLM Extraction

M3 uses an OpenAI-compatible Chat Completions endpoint. Configure it with:

```powershell
$env:LLM_API_KEY="..."
$env:LLM_BASE_URL="https://api.openai.com/v1"
$env:LLM_MODEL="gpt-4o-mini"
$env:ALLOW_MOCK_EXTRACTOR="true"
```

`ALLOW_MOCK_EXTRACTOR=true` allows development fallback when `LLM_API_KEY` is
missing, and also allows `extract_level=mock` for explicit mock extraction.
Set it to `false` in stricter environments so missing LLM configuration returns
`extraction_failed` instead of silently using mock data.

## OpenSPG Ingest

M5 maps `PaperExtractionResult` into graph entities and relations, including
`supportedBy` evidence relations. By default `MOCK_KAG=true`, so ingest returns
local write statistics without calling OpenSPG.

For the current local closed loop, use the OpenSPG compose Neo4j backend:

```powershell
$env:MOCK_KAG="false"
$env:OPENSPG_BASE_URL="http://127.0.0.1:8887"
$env:OPENSPG_ACCOUNT="openspg"
$env:OPENSPG_PASSWORD="openspg123"
$env:OPENSPG_PROJECT_ID="1"
$env:OPENSPG_PROJECT_NAME="LabKAG"
$env:OPENSPG_NAMESPACE="LabKAG"
$env:OPENSPG_WRITE_BACKEND="neo4j"
$env:OPENSPG_NEO4J_URI="neo4j://127.0.0.1:7687"
$env:OPENSPG_NEO4J_USER="neo4j"
$env:OPENSPG_NEO4J_PASSWORD="openspgneo4j"
$env:OPENSPG_NEO4J_DATABASE="neo4j"
```

`POST /v1/papers/ingest` only writes remotely when `confirm=true`.

The HTTP write path remains configurable through `OPENSPG_WRITE_BACKEND=http`
and `OPENSPG_WRITE_PATH`, but the current local OpenSPG image has not exposed a
validated generic graph-write REST endpoint for LabKAG.

## Local OpenSPG Backend

The OpenSPG backend compose stack lives under `deploy/openspg/`:

```powershell
Copy-Item deploy\openspg\.env.example deploy\openspg\.env
docker compose --env-file deploy\openspg\.env -f deploy\openspg\docker-compose.yml up -d
```

The root project does not use Docker Compose for the LabKAG API service yet.

Expected local service endpoints:

- OpenSPG UI/API: `http://127.0.0.1:8887`
- Neo4j Browser: `http://127.0.0.1:7474`
- Neo4j Bolt: `neo4j://127.0.0.1:7687`

Default local credentials used by the compose stack:

- OpenSPG: `openspg` / `openspg123`
- Neo4j: `neo4j` / `openspgneo4j`

## M7 Handoff Check

The M7 verification script performs the reproducible first-version closed loop:

```text
health check
apply LabKAG literature schema
POST /v1/papers/ingest with confirm=true
POST /v1/evidence/search scoped by project_id and paper_id
POST /v1/literature/query scoped by project_id and paper_id
```

It uses fixed `m7_closed_loop_*` IDs and is safe to run repeatedly because graph
writes use idempotent Neo4j `MERGE` operations.
