# LabKAG 概念设计文档

## 0. 文档定位

本文档用于定义 **LabKAG（Laboratory Knowledge Augmented Generation）** 的核心概念、系统边界、系统架构、设计原则、MVP 建设路线与评价指标。

LabKAG 的目标不是简单构建一个“实验室资料聊天机器人”，而是构建面向科学实验室的知识基础设施，使实验室中的文献、实验记录、SOP、样品、仪器、试剂、测量数据、失败案例和人员经验能够被结构化、关联化、检索化、推理化，并最终服务于实验设计、实验执行、实验复现、异常分析和科研决策。

---

## 1. LabKAG 定义

### 1.1 中文定义

**LabKAG**，即 **Laboratory Knowledge Augmented Generation**，是面向科学实验室场景的知识增强生成框架。

它通过将实验室中的多源异构知识，包括科研文献、实验记录、实验方案、样品信息、试剂耗材、仪器数据、测量结果、失败案例、SOP 和人员经验，组织为可追溯、可检索、可推理的实验室知识体系，并结合大语言模型、知识图谱、向量检索、结构化查询和规则推理，为实验室科研活动提供基于证据的智能辅助。

简而言之：

> **LabKAG = 实验室知识图谱 + 科研文献 RAG + 实验记录结构化 + 实验过程追踪 + 实验推理 + 证据追溯。**

LabKAG 的核心不是“让大模型读文档”，而是让大模型在实验室知识体系中完成可靠的检索、关联、推理和生成。

---

### 1.2 英文定义

**LabKAG, or Laboratory Knowledge Augmented Generation, is a laboratory-oriented knowledge-augmented generation framework that integrates scientific literature, experimental records, protocols, samples, reagents, instruments, measurements, datasets, failure cases, and tacit laboratory experience into a provenance-aware knowledge system.**

It combines large language models, knowledge graphs, vector retrieval, structured databases, rule-based reasoning, and evidence tracking to support experimental design, reproducibility checking, anomaly analysis, protocol optimization, and evidence-grounded scientific reasoning.

---

### 1.3 简短定义

> **LabKAG 是面向科学实验室的垂直 KAG 系统，用于把实验室知识从分散文档转化为可计算、可追溯、可复用、可推理的科研知识资产。**

---

## 2. 与相关系统的区别

| 概念 | 核心能力 | 局限 | LabKAG 的差异 |
|---|---|---|---|
| 普通 RAG | 文档切片、向量检索、答案生成 | 缺乏实验实体关系、样品追踪、条件推理 | 强调实验室知识建模、图谱关系、证据链和实验推理 |
| 文献 RAG | 论文问答、摘要、引用定位 | 主要围绕论文，难以连接真实实验记录 | 将文献方法与本实验室实验过程对齐 |
| ELN 电子实验记录 | 记录实验过程 | 多数只是记录与管理，智能推理能力弱 | 在 ELN 之上增加知识图谱、RAG、推理和证据追踪 |
| LIMS | 管理样品、流程、库存、仪器 | 偏管理系统，知识生成与推理能力弱 | 可接入 LIMS，并在其上做知识增强推理 |
| 通用 KAG | 专业领域知识增强问答 | 不一定理解实验室流程和实验对象 | 是针对实验室科研工作流的垂直化 KAG |

---

## 3. LabKAG 的提出背景

科学实验室是典型的知识密集型环境。实验室每天产生大量知识，这些知识既包括显性知识，也包括隐性经验。

### 3.1 实验室知识来源

实验室知识通常来自：

1. **科研文献**：论文 PDF、综述、专利、技术报告、预印本、补充材料。
2. **实验记录**：纸质实验记录、电子实验记录 ELN、Word、Markdown、Notion、Obsidian、实验日志。
3. **SOP 与 Protocol**：标准操作流程、仪器说明、安全规范、内部经验手册。
4. **样品与试剂**：样品编号、批次、来源、制备过程、试剂批号、库存记录。
5. **仪器与测量数据**：仪器型号、参数、校准记录、原始数据文件、图像、光谱、色谱、质谱、传感器数据。
6. **科研过程资料**：组会 PPT、项目计划、研究假设、任务分工、代码仓库、数据分析脚本。
7. **失败案例与隐性经验**：失败实验、异常现象、怀疑原因、修正动作、师兄师姐经验。

---

### 3.2 实验室知识管理痛点

#### 3.2.1 知识分散

论文、实验记录、仪器文件、Excel 表格、SOP 和组会材料分散在不同位置，很难形成统一视图。

#### 3.2.2 文献知识与实验知识脱节

研究者阅读文献后会进行实验复现或改造，但文献方法与本实验室实验之间的关系通常没有被结构化保存。

例如：

```text
Paper A 提出了 Method M
Experiment E 复现了 Method M
Experiment E 修改了反应温度、样品前处理和测量仪器
Result R 与 Paper A 的结论部分一致
```

#### 3.2.3 样品追踪困难

一个样品可能经历多个处理步骤、多个实验和多次测量。如果没有知识图谱式关联，很难回答：

```text
样品 S-2026-001 是如何制备的？
它经历过哪些处理？
由谁操作？
用过哪些试剂？
在哪台仪器上测量？
产生了哪些结果？
和哪些论文方法有关？
```

#### 3.2.4 失败经验难以沉淀

失败实验经常被当作无效记录，但它们包含高价值信息：

- 哪些参数容易导致失败；
- 哪些试剂批次可能有问题；
- 哪些仪器状态会影响结果；
- 哪些 protocol 描述不完整；
- 哪些条件组合不应重复尝试。

#### 3.2.5 实验复现性不足

实验记录中经常缺少关键参数，例如反应温度、反应时间、pH、浓度、转速、离心时间、干燥条件、样品编号、试剂批号、仪器校准状态、原始数据路径和分析脚本。

#### 3.2.6 普通 RAG 难以解决实验室推理问题

普通 RAG 适合问“某篇文档里说了什么”，但不适合稳定回答：

```text
哪个变量最可能导致实验失败？
某个样品经历了哪些处理？
哪批实验与某个异常现象有关？
哪些论文方法被本实验室复现过？
某条实验记录是否足够复现？
```

这些问题需要结构化知识、关系推理、数值比较、时间过滤和证据链，而不仅是语义相似度检索。

---

## 4. LabKAG 的目标

LabKAG 的目标可以分为五层：

1. **知识接入**：统一接入论文、实验记录、SOP、样品表、仪器数据、Excel、图片、代码、失败记录。
2. **知识结构化**：抽取实验实体、参数、条件、结果、结论和证据。
3. **知识关联化**：将文献、实验、样品、试剂、仪器、测量、结果、失败案例、人员和项目建立关系。
4. **知识推理化**：通过图谱推理、规则推理、数值查询、向量检索和 LLM 推理支持复杂科研问题。
5. **知识应用化**：嵌入科研工作流，支持文献理解、实验设计、实验记录、复现检查、失败分析、SOP 审计、项目复盘和新成员培训。

---

## 5. LabKAG 总体系统架构

LabKAG 可设计为八层架构：

```text
┌──────────────────────────────────────────────┐
│ 8. 应用层：实验室智能助手与科研工作流界面        │
├──────────────────────────────────────────────┤
│ 7. 生成与交互层：答案生成、报告生成、证据展示     │
├──────────────────────────────────────────────┤
│ 6. 检索与推理层：混合检索、图谱推理、规则推理     │
├──────────────────────────────────────────────┤
│ 5. 知识服务层：实体服务、样品服务、实验服务       │
├──────────────────────────────────────────────┤
│ 4. 知识存储层：关系库、图数据库、向量库、对象存储 │
├──────────────────────────────────────────────┤
│ 3. 知识建模层：Lab Ontology、Schema、规则体系    │
├──────────────────────────────────────────────┤
│ 2. 解析抽取层：文档解析、信息抽取、结构化校验     │
├──────────────────────────────────────────────┤
│ 1. 数据接入层：论文、ELN、SOP、仪器、样品、数据   │
└──────────────────────────────────────────────┘
```

这八层不是必须一次性全部实现，但它们构成完整 LabKAG 的参考架构。

---

## 6. 数据接入层

### 6.1 数据接入目标

数据接入层负责将实验室所有知识源接入系统，并为每个数据源建立统一索引和来源信息。

### 6.2 数据类型

| 数据类型 | 示例 | 处理方式 |
|---|---|---|
| PDF | 论文、专利、说明书 | 文本抽取、版面解析、表格抽取 |
| 文档 | Word、Markdown、Notion 导出 | 结构化解析 |
| 表格 | Excel、CSV | 表格读取、字段映射 |
| 图片 | 显微图、实验照片 | 元数据保存、图像关联 |
| 仪器数据 | 光谱、色谱、质谱、传感器文件 | 文件索引、元数据抽取 |
| 代码 | Python、R、Jupyter Notebook | 脚本关联、结果追踪 |
| 数据库 | ELN、LIMS、库存系统 | API 或数据库同步 |
| 人工记录 | 实验日志、失败案例 | LLM 抽取 + 人工确认 |

### 6.3 来源信息 Provenance

每个数据片段都应该保留来源信息：

```text
source_id
source_type
file_name
file_path
page_number
sheet_name
row_number
chunk_id
created_at
updated_at
operator
experiment_id
sample_id
project_id
instrument_id
version
checksum
```

Provenance 是 LabKAG 的基础。如果一个答案无法追溯来源，那么它只能作为模型推测，不能作为实验决策依据。

---

## 7. 解析与抽取层

### 7.1 解析目标

解析与抽取层负责将非结构化或半结构化数据转化为结构化知识。

### 7.2 文献解析

对论文和文献资料，需要抽取：

```text
title
authors
affiliations
year
journal
doi
abstract
keywords
methods
materials
experimental_conditions
results
metrics
conclusions
references
figures
tables
supplementary_materials
```

### 7.3 实验记录解析

对实验记录，需要抽取：

```text
experiment_id
experiment_title
project
operator
date
purpose
hypothesis
protocol
steps
samples
reagents
instruments
parameters
conditions
observations
measurements
results
conclusions
anomalies
failure_reason
raw_data_files
analysis_scripts
```

### 7.4 SOP 与 Protocol 解析

对 SOP 和 protocol，需要抽取：

```text
protocol_id
protocol_name
applicable_scope
required_materials
required_reagents
required_instruments
steps
critical_parameters
safety_notes
quality_control
expected_outputs
common_failures
```

### 7.5 信息抽取策略

推荐采用混合抽取策略：

```text
规则解析
+ 专用解析器
+ LLM 结构化抽取
+ JSON Schema 校验
+ 人工确认
```

典型流程：

```text
原始文档
-> 文本与表格解析
-> 分块
-> LLM 按 schema 抽取
-> JSON Schema / Pydantic 校验
-> 置信度评分
-> 人工确认
-> 入库
```

---

## 8. 知识建模层：Lab Ontology 与 Schema

### 8.1 Schema First 原则

LabKAG 的核心不是模型，而是实验室知识建模。

如果没有清晰 schema，系统会退化成普通 RAG；如果 schema 过于粗糙，系统无法支持样品追踪、实验复现、失败归因和参数比较。

### 8.2 通用实体模型

LabKAG 的通用实体可以包括：

```text
Paper
Project
ResearchQuestion
Hypothesis
Experiment
Protocol
Step
Sample
Material
Reagent
Instrument
Parameter
Condition
Measurement
Dataset
Observation
Result
Conclusion
FailureCase
Anomaly
Cause
CorrectiveAction
Evidence
Person
Organization
File
```

### 8.3 核心关系模型

核心关系可以包括：

```text
Project contains Experiment
Project investigates ResearchQuestion
ResearchQuestion motivates Hypothesis
Experiment tests Hypothesis
Experiment follows Protocol
Protocol contains Step
Experiment has_step Step
Experiment uses Sample
Experiment uses Material
Experiment uses Reagent
Experiment uses Instrument
Experiment has_parameter Parameter
Experiment has_condition Condition
Experiment produces Measurement
Measurement generates Dataset
Dataset supports Result
Result supports Conclusion
Result supports_or_refutes Hypothesis
Experiment has_observation Observation
Experiment has_failure FailureCase
FailureCase has_anomaly Anomaly
FailureCase has_suspected_cause Cause
FailureCase has_corrective_action CorrectiveAction
Person performed Experiment
Person authored Paper
Paper reports Protocol
Paper reports Result
Paper supports Hypothesis
File provides Evidence
Evidence supports Result
Evidence supports Conclusion
```

### 8.4 学科扩展 Schema

不同实验室可以在通用 schema 上进行扩展。

**生物实验室**

```text
CellLine
Gene
Protein
Antibody
Plasmid
CultureCondition
Assay
Medium
IncubationCondition
```

**化学实验室**

```text
Compound
Reaction
Catalyst
Solvent
Yield
Purification
ReactionCondition
SpectralData
```

**材料实验室**

```text
Material
Synthesis
Characterization
CrystalStructure
Morphology
Property
PerformanceMetric
Device
```

**计算实验室**

```text
Dataset
Model
Algorithm
Hyperparameter
TrainingRun
EvaluationMetric
Benchmark
CodeVersion
```

### 8.5 实验过程链模型

实验室知识的核心是过程，而不是孤立文档。LabKAG 应显式建模实验过程链：

```text
ResearchQuestion
-> Hypothesis
-> Protocol
-> Experiment
-> Sample
-> Measurement
-> Dataset
-> Result
-> Conclusion
-> NextExperiment
```

---

## 9. 知识存储层

### 9.1 混合存储架构

LabKAG 不应使用单一数据库承载所有数据。推荐采用混合存储：

```text
关系数据库
+ 图数据库
+ 向量数据库
+ 对象存储
+ 搜索引擎
+ 可选时序数据库
```

### 9.2 各类存储职责

| 存储组件 | 负责内容 | 示例 |
|---|---|---|
| 关系数据库 | 结构化元数据 | 实验表、样品表、人员表、项目表 |
| 图数据库 | 实体关系、多跳路径 | 样品追踪、文献-实验关联、实验链 |
| 向量数据库 | 文档 chunk 语义检索 | 论文段落、实验记录、SOP |
| 对象存储 | 原始文件 | PDF、图片、仪器数据、脚本 |
| 搜索引擎 | 关键词检索 | 标题、编号、术语、标签 |
| 时序数据库 | 仪器传感器时间序列 | 温度、湿度、压力、实时测量数据 |

### 9.3 MVP 推荐技术组合

MVP 阶段可以采用：

```text
PostgreSQL + pgvector + Neo4j + MinIO
```

或：

```text
PostgreSQL + pgvector + OpenSPG + 本地对象存储
```

其中：

- PostgreSQL 保存结构化数据；
- pgvector 保存文本 embedding；
- Neo4j / OpenSPG 保存实验室知识图谱；
- MinIO / 文件系统保存原始文件；
- Python 服务负责解析、抽取、入库和检索编排。

---

## 10. 知识服务层

知识服务层向上提供标准化 API，使应用层不直接访问底层数据库。

### 10.1 核心服务

可以包括：

```text
DocumentService
PaperService
ExperimentService
SampleService
ProtocolService
InstrumentService
ReagentService
MeasurementService
ResultService
FailureCaseService
EvidenceService
GraphQueryService
HybridSearchService
```

### 10.2 服务职责示例

#### SampleService

```text
get_sample(sample_id)
get_sample_lineage(sample_id)
get_related_experiments(sample_id)
get_measurements(sample_id)
get_failures(sample_id)
```

#### ExperimentService

```text
get_experiment(experiment_id)
get_experiment_steps(experiment_id)
get_experiment_parameters(experiment_id)
get_experiment_results(experiment_id)
compare_experiments(experiment_id_a, experiment_id_b)
```

#### EvidenceService

```text
get_evidence(evidence_id)
trace_answer_sources(answer_id)
get_file_location(source_id)
get_citation_context(source_id)
```

知识服务层的价值在于把底层复杂存储封装成面向实验室对象的能力。

---

## 11. 检索与推理层

### 11.1 检索目标

LabKAG 的检索不是单一向量召回，而是混合检索：

```text
关键词检索
+ 向量检索
+ 图谱检索
+ 结构化查询
+ 数值过滤
+ 时间过滤
+ 权限过滤
+ 证据回溯
```

### 11.2 检索策略选择

| 用户问题 | 推荐检索方式 |
|---|---|
| “这篇论文主要讲了什么？” | 文档 chunk 向量检索 + 摘要生成 |
| “样品 S-001 经历了什么？” | 图谱检索 + 结构化查询 |
| “哪些实验温度超过 80°C？” | 结构化查询 |
| “哪些失败案例和 pH 有关？” | 图谱检索 + 关键词检索 |
| “这个异常以前出现过吗？” | 失败案例向量检索 + 图谱检索 |
| “我们复现 Paper A 时改了哪些条件？” | 文献抽取结果 + 实验图谱 + 参数比较 |
| “哪个变量最可能影响结果？” | 结构化统计 + 图谱路径 + LLM 解释 |

### 11.3 推理类型

LabKAG 至少需要支持五类推理。

#### 图谱推理

用于样品追踪、实验过程链、文献-实验关联、多跳关系查询。

```text
Sample S -> prepared_by Experiment E1
Experiment E1 -> uses Reagent R
Experiment E1 -> produces Sample S2
Sample S2 -> measured_by Experiment E2
Experiment E2 -> produces Result R2
```

#### 规则推理

用于复现性检查、SOP 审计、安全规则检查、数据完整性检查。

```text
如果 Experiment.type = chemical_reaction
则必须包含 temperature、time、reagent、solvent、sample_id、operator、raw_data_file。
```

#### 数值推理

用于参数范围查询、指标排序、条件比较、趋势分析。

```text
找出所有温度在 70-90°C 且产率高于 80% 的实验。
```

#### 语义推理

用于同义表达、文本归纳、复杂问题理解。

```text
“反应没跑出来”“无目标产物”“产率为 0”可能都属于失败异常类型：NoProduct。
```

#### 证据融合推理

用于将多个来源的证据合并成答案。

```text
文献 A 支持条件 X；
实验 E1 在条件 X 下成功；
实验 E2 在条件 Y 下失败；
系统综合判断：当前实验更接近 E2，失败风险较高。
```

### 11.4 推理编排流程

典型问答流程：

```text
用户问题
-> 意图识别
-> 实体识别
-> 查询计划生成
-> 权限检查
-> 图谱检索
-> 向量检索
-> 结构化查询
-> 数值与规则校验
-> 证据排序
-> 答案生成
-> 证据展示
-> 人工反馈
```

---

## 12. 生成与交互层

生成与交互层负责将检索和推理结果转化为用户可理解、可操作、可追溯的输出。

推荐输出格式：

```text
结论：
证据：
推理过程：
缺失信息：
不确定性：
建议：
相关实验：
相关文献：
```

每条关键结论应关联证据：

```text
结论 C
-> Evidence E1: Paper A, page 5, Method section
-> Evidence E2: Experiment E-2026-014, step 3
-> Evidence E3: Dataset D-2026-009, row 12
```

LabKAG 必须明确区分：

```text
已证实
较可能
推测
缺少证据
存在冲突证据
需要人工确认
```

---

## 13. 应用层

LabKAG 可以形成多个实验室智能助手。

### 13.1 文献助手

- 论文摘要；
- 方法抽取；
- 实验条件抽取；
- 指标对比；
- 文献卡片生成；
- 文献之间的异同分析；
- 文献方法到实验室 protocol 的映射。

### 13.2 实验设计助手

- 根据研究目标推荐 protocol；
- 根据文献和历史实验推荐参数范围；
- 识别高风险参数；
- 给出对照组建议；
- 生成实验计划草案；
- 检查实验方案是否缺少关键条件。

### 13.3 实验记录助手

- 将自然语言实验记录转成结构化记录；
- 自动识别样品、试剂、仪器和参数；
- 提醒缺失字段；
- 自动关联原始数据；
- 生成规范化实验摘要。

### 13.4 实验复现助手

- 检查实验记录是否满足复现条件；
- 对比文献 protocol 与实验室 protocol；
- 标记缺失参数；
- 提醒不一致条件；
- 生成复现风险评估。

### 13.5 异常分析助手

- 检索相似失败案例；
- 比较成功与失败条件；
- 分析异常可能原因；
- 建议验证实验；
- 生成异常复盘报告。

### 13.6 SOP 助手

- 生成 SOP 草案；
- 审计 SOP 缺失项；
- 根据失败案例更新 SOP；
- 标记关键参数和安全注意事项；
- 比较不同版本 SOP 的变化。

### 13.7 项目助手

- 追踪研究问题、假设、实验、结果、结论；
- 生成项目进展摘要；
- 发现未验证假设；
- 汇总支持或反驳某个结论的证据；
- 辅助组会汇报。

### 13.8 样品与库存助手

- 样品生命周期追踪；
- 试剂批次关联；
- 仪器使用记录关联；
- 查询某个样品参与过哪些实验；
- 查询某批试剂是否与失败实验相关。

---

## 14. LabKAG 核心流程

### 14.1 数据入库流程

```text
原始数据上传
-> 文件类型识别
-> 元数据登记
-> 文本/表格/图片解析
-> chunk 生成
-> embedding 生成
-> LLM 结构化抽取
-> schema 校验
-> 人工确认
-> 关系构建
-> 入库
-> 建立证据索引
```

### 14.2 用户问答流程

```text
用户提出问题
-> 识别问题类型
-> 识别实体和约束
-> 生成查询计划
-> 多源检索
-> 证据筛选
-> 结构化推理
-> LLM 生成答案
-> 返回结论、证据和不确定性
```

### 14.3 实验记录结构化流程

```text
用户输入实验记录
-> 识别实验类型
-> 匹配 protocol
-> 抽取步骤、样品、试剂、参数
-> 检查缺失字段
-> 生成结构化 JSON
-> 人工确认
-> 入库并关联图谱
```

### 14.4 失败案例沉淀流程

```text
实验标记为失败
-> 抽取异常现象
-> 抽取相关参数
-> 关联样品、试剂、仪器
-> 检索相似失败案例
-> 人工填写或确认怀疑原因
-> 记录修正动作
-> 追踪后续实验结果
-> 更新 FailureCase 图谱
```

---

## 15. 设计原则

### 15.1 Provenance First：来源优先

LabKAG 中的每个实体、关系、结论和答案都应可追溯来源。

系统必须能够回答：

```text
这个结论来自哪里？
来自哪篇论文？
哪一页？
哪个实验记录？
哪个样品？
哪个仪器文件？
哪个操作者？
哪个时间点？
是否经过人工确认？
```

没有来源的结论不能作为实验决策依据。

---

### 15.2 Schema First：模型先行

LabKAG 首先是知识建模问题，其次才是大模型应用问题。

必须先定义：

- 实验对象；
- 实验过程；
- 样品关系；
- 参数结构；
- 结果类型；
- 失败类型；
- 证据模型；
- 权限模型。

否则系统会退化成不可控的文档问答。

---

### 15.3 Human-in-the-loop：关键节点人工确认

实验室知识系统不能完全依赖自动抽取。

以下内容应支持人工确认：

- 关键参数；
- 实验结果；
- 失败原因；
- SOP 修改；
- 高风险建议；
- 结论归纳；
- 数据异常解释；
- 文献方法与实验方法的映射。

---

### 15.4 Failure Knowledge is First-class：失败知识一等建模

失败实验不是垃圾数据，而是实验室最有价值的知识资产之一。

LabKAG 应显式建模：

```text
FailureCase
Anomaly
SuspectedCause
CorrectiveAction
RelatedParameter
RelatedSample
RelatedProtocol
Evidence
```

---

### 15.5 Numerical Awareness：数值敏感

实验室知识高度依赖数值。LabKAG 必须支持：

- 单位规范化；
- 数值范围查询；
- 参数比较；
- 指标排序；
- 表格抽取；
- 曲线元数据关联；
- 条件与结果之间的统计分析。

---

### 15.6 Evidence-grounded Generation：基于证据生成

LLM 生成的答案必须受到证据约束。

推荐规则：

```text
没有证据，不给确定结论；
证据不足，明确说明缺失项；
证据冲突，展示冲突来源；
涉及实验安全，必须提示人工确认；
涉及参数建议，必须说明依据。
```

---

### 15.7 Workflow Integration：嵌入实验工作流

LabKAG 不应是孤立聊天窗口，而应接入实验室实际流程：

- 文献管理；
- 实验记录；
- 样品管理；
- 仪器排期；
- 数据分析；
- SOP 维护；
- 项目复盘；
- 组会汇报。

---

### 15.8 Incremental Construction：增量建设

实验室知识系统不能一次性完成。应允许逐步建设：

```text
先接入文献和实验记录；
再建立样品和实验关系；
再加入失败案例；
再加入仪器数据；
再加入复杂推理和决策支持。
```

---

### 15.9 Domain Adaptability：领域可扩展

不同实验室的 schema 差异很大。LabKAG 应采用：

```text
通用核心 schema
+ 学科扩展 schema
+ 实验室自定义字段
+ 人工校验规则
```

---

### 15.10 Safety and Compliance：安全合规

涉及实验安全、化学品、生物安全、数据隐私和知识产权的内容，必须有权限管理和审核机制。

---

## 16. MVP 设计

### 16.1 MVP 定位

LabKAG 的 MVP 不应追求“大而全”，而应优先验证实验室知识增强的核心价值。

推荐 MVP 定位：

> **围绕论文、实验记录、样品编号、实验结果和失败案例，构建一个可追溯的实验室知识问答与实验追踪系统。**

### 16.2 MVP 数据范围

建议第一阶段接入：

```text
100 篇以内核心论文
100-500 条实验记录
10-30 个 SOP / protocol
样品编号表
实验结果表
失败实验记录
相关原始数据索引
```

### 16.3 MVP Schema

最小实体：

```text
Paper
Experiment
Protocol
Sample
Reagent
Instrument
Parameter
Measurement
Result
FailureCase
Evidence
Person
```

最小关系：

```text
Paper reports Protocol
Paper reports Result
Experiment follows Protocol
Experiment uses Sample
Experiment uses Reagent
Experiment uses Instrument
Experiment has_parameter Parameter
Experiment produces Measurement
Measurement supports Result
Experiment has_failure FailureCase
Evidence supports Result
Person performed Experiment
```

### 16.4 MVP 核心功能

#### 功能一：样品追踪

输入：样品编号。

输出：

```text
样品来源
制备过程
关联实验
使用试剂
测量记录
实验结果
异常记录
证据文件
```

#### 功能二：文献方法对齐

输入：论文、protocol 或实验编号。

输出：

```text
文献方法
本实验室复现实验
参数差异
结果差异
证据来源
```

#### 功能三：失败案例检索

输入：当前实验异常描述。

输出：

```text
相似失败案例
共同参数
可能原因
修正动作
相关证据
```

#### 功能四：实验记录复现性检查

输入：实验记录。

输出：

```text
完整性评分
缺失字段
风险项
需要补充的信息
是否满足复现要求
```

#### 功能五：证据支撑问答

输入：自然语言问题。

输出：

```text
答案
证据
来源
推理路径
不确定性
```

---

## 17. 技术路线建议

### 17.1 后端技术栈

MVP 可采用：

```text
Python / FastAPI
PostgreSQL
pgvector
Neo4j 或 OpenSPG
MinIO / 本地文件系统
Redis
Celery / RQ
```

### 17.2 文档解析

可选工具：

```text
GROBID：论文元数据与参考文献解析
PyMuPDF：PDF 文本与版面解析
pdfplumber：PDF 表格与文本解析
Camelot / Tabula：表格抽取
python-docx：Word 文档解析
pandas：Excel / CSV 解析
```

### 17.3 LLM 抽取

建议采用结构化输出：

```json
{
  "experiment_id": "E-2026-001",
  "purpose": "...",
  "samples": [],
  "reagents": [],
  "instruments": [],
  "parameters": [],
  "results": [],
  "evidence": []
}
```

并配合：

```text
JSON Schema
Pydantic
字段置信度
人工确认状态
```

### 17.4 检索技术

推荐组合：

```text
BM25 / 关键词检索
向量检索
图谱查询
SQL 查询
元数据过滤
rerank
```

### 17.5 前端界面

MVP 前端可以包含：

- 文档上传页；
- 实验记录录入页；
- 样品追踪页；
- 失败案例页；
- 问答界面；
- 证据查看器；
- 人工确认界面。

---

## 18. 路线图

### 阶段一：文档与实验记录接入

目标：

- 接入论文 PDF；
- 接入实验记录；
- 接入 SOP；
- 建立统一文件索引；
- 完成基础 chunk；
- 建立来源追踪。

输出：

```text
Document Index
Chunk Store
Metadata Table
Source Registry
```

---

### 阶段二：元数据与实验实体抽取

目标：

- 抽取论文标题、作者、年份、DOI、摘要；
- 抽取实验目的、步骤、参数、样品、仪器、结果；
- 建立 JSON Schema；
- 增加人工确认界面。

输出：

```text
Paper Metadata
Experiment Metadata
Sample Table
Protocol Table
Parameter Table
Result Table
```

---

### 阶段三：实验室知识图谱

目标：

- 建立实体关系；
- 支持样品追踪；
- 支持实验过程链；
- 支持文献方法与实验方法对齐；
- 支持实验结果证据链。

输出：

```text
Lab Knowledge Graph
Sample Lineage Graph
Experiment-Result Graph
Paper-Protocol-Experiment Graph
```

---

### 阶段四：混合检索与问答

目标：

- 实现关键词检索；
- 实现向量检索；
- 实现图谱检索；
- 实现元数据过滤；
- 实现证据融合；
- 输出可追溯答案。

输出：

```text
Hybrid Retriever
Evidence-grounded QA
Reasoning Path
Citation System
```

---

### 阶段五：实验推理与决策支持

目标：

- 实现实验复现性检查；
- 实现失败案例检索；
- 实现异常归因；
- 实现参数建议；
- 实现 SOP 审计；
- 实现实验复盘报告生成。

输出：

```text
Reproducibility Checker
Failure Case Analyzer
Anomaly Reasoner
Protocol Advisor
Experiment Review Generator
```

---

## 19. 评价指标

### 19.1 抽取质量

```text
实体抽取准确率
关系抽取准确率
参数抽取准确率
单位规范化准确率
表格抽取准确率
证据定位准确率
```

### 19.2 检索质量

```text
文档召回率
实体召回率
证据定位准确率
多跳路径正确率
相似失败案例召回率
```

### 19.3 推理质量

```text
复现性检查准确率
异常归因合理性
参数建议可用性
结论证据一致性
幻觉率
不确定性表达质量
```

### 19.4 实验室价值

```text
查找历史实验时间减少
实验记录完整性提升
失败案例复用率
SOP 更新效率
新成员上手时间减少
实验复现成功率提升
```

---

## 20. 风险与边界

### 20.1 LLM 幻觉风险

LabKAG 必须防止模型生成没有证据支持的结论。

### 20.2 实验安全风险

涉及化学品、生物安全、高温高压、危险仪器等实验建议时，必须加入安全规则和人工审核。

### 20.3 数据质量风险

实验记录本身可能不完整、不规范或存在错误。系统不能默认所有输入都可靠。

### 20.4 知识产权与隐私风险

实验数据、未发表论文、项目计划和内部 SOP 可能涉及敏感信息，需要权限管理。

### 20.5 过度自动化风险

LabKAG 应辅助科研人员，而不是替代科学判断。

### 20.6 跨学科泛化风险

不同实验室差异很大，不能用一个固定 schema 覆盖所有场景。

---

## 21. 总结

LabKAG 是面向科学实验室的知识增强生成框架。它的意义在于将实验室中分散的文献、实验记录、SOP、样品、试剂、仪器、数据和失败案例整合成一个可追溯、可检索、可推理的知识系统。

与普通 RAG 相比，LabKAG 更重视：

```text
实验室知识建模
样品与实验过程追踪
文献方法与实验室实践对齐
失败实验沉淀
实验复现性检查
参数、条件和结果之间的结构化关系
基于证据的科研推理
```

与通用 KAG 相比，LabKAG 更关注科学实验室的实际工作流，目标不是泛化问答，而是支持实验设计、实验执行、实验记录、结果解释、异常分析和知识复用。

一个可落地的 LabKAG 应从 MVP 开始：

```text
论文 + 实验记录 + 样品编号 + 结果数据 + 失败案例
```

优先跑通：

```text
样品追踪
文献方法对齐
失败案例检索
实验复现性检查
证据支撑问答
```

当这些能力稳定后，LabKAG 才能真正成为实验室的知识基础设施，而不仅仅是一个接入文档的大模型聊天工具。
