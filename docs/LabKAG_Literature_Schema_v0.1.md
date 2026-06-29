# LabKAG Literature Schema v0.1

## Entities

```text
Paper
Author
Institution
ResearchObject
ResearchProblem
Method
Material
ExperimentCondition
Metric
Result
Conclusion
Evidence
```

## Minimum Implemented Entity Types

The first framework pass includes Pydantic support and mock graph mapping for:

```text
Paper
Method
Material
Result
Conclusion
Evidence
```

## Minimum Relations

```text
Paper proposes Method
Paper uses Material
Paper reports Result
Paper draws_conclusion Conclusion
Result supported_by Evidence
Conclusion supported_by Evidence
```

## Evidence Fields

```text
evidence_id
document_id
chunk_id
page
section_title
source_text
offset_start
offset_end
paper_id
```
