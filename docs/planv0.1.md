**LabKAG v0.1 第一版实现框架计划**

**目标：** 先搭出一个可运行、可测试的 FastAPI Skill Server 骨架，跑通最小链路：`health -> upload -> parse -> chunk -> extract mock -> evidence bind -> query/search mock`。OpenSPG/KAG 第一版先做 Adapter 接口和 mock/stub，不直接硬接真实服务。

**技术栈：**

```text
Python 3.10
FastAPI
Pydantic v2
Uvicorn
pytest
PyMuPDF
python-dotenv
ruff
```

**阶段 1：项目基础框架**

1. 配置 `pyproject.toml`
   - Python 版本：`>=3.10,<3.11`
   - pytest、ruff 基础配置
   - 包名使用 `app`

2. 配置 `requirements.txt`
   - `fastapi`
   - `uvicorn[standard]`
   - `pydantic`
   - `pydantic-settings`
   - `python-dotenv`
   - `PyMuPDF`
   - `pytest`
   - `ruff`

3. 实现 `app/config.py`
   - 读取环境变量
   - 配置 `APP_NAME`
   - 配置 `DATA_DIR`
   - 配置 `UPLOAD_DIR`
   - 配置 `PARSED_DIR`
   - 配置 `EXTRACTION_DIR`
   - 配置 `MOCK_KAG=true`

4. 实现 `app/main.py`
   - 创建 FastAPI app
   - 注册 health、papers、literature、evidence 路由
   - 暴露 OpenAPI

**阶段 2：统一数据结构**

1. `app/schemas/response.py`
   - 定义统一 `SkillResponse`
   - 字段：`status`、`data`、`evidence`、`warnings`、`errors`、`metadata`

2. `app/schemas/errors.py`
   - 定义错误码常量或枚举：
     - `file_not_found`
     - `unsupported_file_type`
     - `parse_failed`
     - `extraction_failed`
     - `schema_validation_failed`
     - `evidence_binding_failed`
     - `openspg_write_failed`
     - `kag_query_failed`
     - `internal_error`

3. `app/schemas/document.py`
   - `DocumentPage`
   - `DocumentChunk`
   - `ParsedDocument`

4. `app/schemas/evidence.py`
   - `Evidence`

5. `app/schemas/extraction.py`
   - `PaperMetadata`
   - `ExtractedMethod`
   - `ExtractedMaterial`
   - `ExtractedCondition`
   - `ExtractedMetric`
   - `ExtractedResult`
   - `ExtractedConclusion`
   - `PaperExtractionResult`

**阶段 3：最小 API 路由**

1. `GET /health`
   - 返回服务状态、版本、mock 模式

2. `POST /v1/papers/upload`
   - 接收 PDF 文件
   - 保存到 `data/uploads`
   - 返回 `file_id`

3. `POST /v1/papers/extract`
   - 输入 `file_id`
   - 调用 PDF parser
   - 调用 chunker
   - 调用 mock extractor
   - 调用 evidence binder
   - 返回 `paper_extraction`

4. `POST /v1/papers/ingest`
   - 第一版只做 dry-run/mock
   - 返回模拟实体数、关系数、evidence 数

5. `POST /v1/literature/query`
   - 第一版调用 mock KAG query adapter
   - 返回固定结构 answer + evidence

6. `POST /v1/evidence/search`
   - 第一版从 extraction mock 或 parsed 数据中检索 evidence
   - 返回 evidence 列表

7. `GET /v1/papers/{paper_id}/knowledge`
   - 第一版返回 mock 或本地 extraction JSON

**阶段 4：核心服务实现**

1. `app/storage/file_store.py`
   - 保存上传文件
   - 根据 `file_id` 找文件
   - 限制文件类型为 `.pdf`

2. `app/storage/metadata_store.py`
   - 第一版用本地 JSON 存储 metadata
   - 不引入数据库

3. `app/services/pdf_parser.py`
   - 使用 PyMuPDF 解析文本型 PDF
   - 输出 pages

4. `app/services/chunker.py`
   - 按页和字符长度生成 chunk
   - 保留 `document_id`、`chunk_id`、`page`、`text`

5. `app/services/paper_extractor.py`
   - 第一版实现 mock/规则抽取
   - 从第一页简单提取 title 候选
   - methods/materials/results/conclusions 先返回可验证的占位结构，但必须绑定 chunk evidence

6. `app/services/evidence_binder.py`
   - 确保 Result / Conclusion 至少绑定一个 Evidence
   - 缺失时返回 warning 和 `needs_review`

7. `app/services/skill_orchestrator.py`
   - 编排 `extract_paper`
   - 编排 `ingest_paper`
   - 保持 API 层薄一些

**阶段 5：OpenSPG/KAG 适配边界**

1. `app/adapters/openspg_mapper.py`
   - 把 `PaperExtractionResult` 映射为实体和关系结构
   - 第一版只生成 Python dict，不写真实 OpenSPG

2. `app/adapters/openspg_client.py`
   - 定义 `write_entities_relations`
   - 第一版 mock 返回统计结果

3. `app/adapters/kag_client.py`
   - 定义 `query`
   - 第一版 mock 返回 evidence-aware answer

4. `app/adapters/kag_query_adapter.py`
   - 封装 `query_literature`
   - 封装 `search_evidence`

**阶段 6：测试优先级**

第一版至少要有这些测试：

```text
tests/test_health.py
tests/test_pdf_parser.py
tests/test_chunker.py
tests/test_extraction_schema.py
tests/test_evidence_binder.py
tests/test_skill_api.py
```

测试目标：

1. `GET /health` 返回 `success`
2. chunker 能保留 page/chunk_id
3. `PaperExtractionResult` schema 能校验
4. evidence binder 能给 result/conclusion 绑定 evidence
5. `/v1/papers/extract` 在 mock 模式下返回统一结构
6. `/v1/evidence/search` 返回 evidence 数组

**阶段 7：开发顺序**

推荐按这个顺序做：

```text
1. pyproject / requirements / config
2. schemas
3. health API
4. file_store + upload API
5. pdf_parser
6. chunker
7. paper_extractor mock
8. evidence_binder
9. extract_paper orchestrator
10. ingest_paper mock
11. query_literature mock
12. search_evidence mock
13. examples
14. README / API 文档
15. 全量 pytest + ruff
```

**第一版边界**

第一版暂时不做：

```text
真实 OpenSPG 写入
真实 KAG 推理
真实 LLM 抽取
数据库
认证权限
OCR
复杂表格解析
前端 UI
```
