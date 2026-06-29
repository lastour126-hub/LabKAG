# LabKAG API v0.1

All Skill endpoints return:

```json
{
  "status": "success",
  "data": {},
  "evidence": [],
  "warnings": [],
  "errors": [],
  "metadata": {
    "request_id": "req_xxx",
    "project_id": "labkag_demo",
    "created_at": "2026-06-29T00:00:00Z"
  }
}
```

## Routes

```text
GET  /health
POST /v1/papers/upload
POST /v1/papers/extract
POST /v1/papers/ingest
GET  /v1/papers/{paper_id}/knowledge
POST /v1/literature/query
POST /v1/evidence/search
```

## Upload

`POST /v1/papers/upload`

Multipart field:

```text
file=<paper.pdf>
```

## Extract

`POST /v1/papers/extract`

```json
{
  "file_id": "file_xxx",
  "project_id": "labkag_demo",
  "extract_level": "basic",
  "return_chunks": false
}
```

## Ingest

`POST /v1/papers/ingest`

```json
{
  "project_id": "labkag_demo",
  "paper_extraction": {},
  "confirm": true
}
```

The first framework version uses a mock OpenSPG client.

## Query Literature

`POST /v1/literature/query`

```json
{
  "question": "What does this paper report?",
  "project_id": "labkag_demo",
  "paper_id": "paper_001",
  "top_k": 5
}
```

## Search Evidence

`POST /v1/evidence/search`

```json
{
  "query": "catalytic activity",
  "project_id": "labkag_demo",
  "entity_types": ["Result"],
  "top_k": 10
}
```
