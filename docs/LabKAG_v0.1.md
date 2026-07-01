# LabKAG v0.1

## 定位

LabKAG v0.1 是一个面向文献处理的 KAG Skill Server。它对外提供稳定的 Skill API，对内使用 Neo4j 保存文献知识图谱和证据。

核心目标：

```text
上传论文
解析 PDF
抽取结构化文献知识
绑定 Evidence
写入 Neo4j
检索 Evidence
回答文献问题
```

## 架构

```text
Client / Agent
-> LabKAG FastAPI Skill Server
-> PDF Parser / Chunker
-> LLM or Mock Extractor
-> Evidence Binder
-> Graph Mapper
-> Neo4j Graph Store
-> Neo4j Query Store
```

## 核心 API

```text
GET  /health
POST /v1/papers/upload
POST /v1/papers/extract
POST /v1/papers/ingest
GET  /v1/papers/{paper_id}/knowledge
POST /v1/evidence/search
POST /v1/literature/query
```

## 文献图模型

实体：

```text
Paper
Method
Material
Condition
Metric
Result
Conclusion
Evidence
```

关系：

```text
Paper -> Method
Paper -> Material
Paper -> Condition
Paper -> Metric
Paper -> Result
Paper -> Conclusion
Paper -> Evidence
Method / Material / Condition / Metric / Result / Conclusion -> Evidence
```

## 运行配置

```env
MOCK_KAG=false
GRAPH_BACKEND=neo4j
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=labkagneo4j
NEO4J_DATABASE=neo4j
```

## 部署

Neo4j 本地部署：

```powershell
docker compose -f deploy\neo4j\docker-compose.yml up -d
```

验证闭环：

```powershell
py -3.10 scripts\verify_m8_neo4j_closed_loop.py
```

## 错误码

```text
file_not_found
unsupported_file_type
parse_failed
extraction_failed
schema_validation_failed
evidence_binding_failed
graph_write_failed
kag_query_failed
internal_error
```

## 当前限制

```text
仅支持文本型 PDF
暂不支持 OCR
暂不支持复杂表格/图片理解
当前 evidence search 是关键词检索
当前 literature query 是基于 Evidence 原文的朴素回答
暂未实现 embedding / vector search
暂未实现 LLM answer synthesis
```

## 后续阶段

M9 重点：

```text
EmbeddingProvider
Evidence embedding
Neo4j vector index
keyword + vector hybrid search
带证据引用的 LLM answer synthesis
```
