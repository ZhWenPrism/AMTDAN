# Data interface

The public contracts are implemented in [`amtdan/datasets/schema.py`](../amtdan/datasets/schema.py).

## Examination record

| Field | Contract |
|:---|:---|
| `patient_id`, `exam_id` | Non-empty study tokens without whitespace |
| `site` | Non-empty site value |
| `modality` | `ModalityState` with visual and clinical availability |
| `clinical_features` | Named finite measurements or `None` |
| `severity_labels` | Named grades from 0 to 4, or `None` |

The clinical-feature and severity-label mappings are copied into read-only mappings. A missing label remains `None`.

## Modality state

At least one of `visual_available` and `clinical_available` is true. The optional `visual_quality` value lies in [0, 1]. The model design uses ultrasound representations and 39 clinical measurements; the public record stores modality metadata and a named feature mapping.

## Task registry

`TaskSpec` supplies a task name and five unique ordered label names. `TaskRegistry` contains exactly 17 uniquely named tasks and provides `by_name` lookup. Constructor inputs are captured as tuples so later changes to caller-owned lists do not alter the validated registry.

## Study-level alignment

Repeated examinations from one patient share a split. Visual and clinical records refer to the same examination window. Units, acquisition metadata and annotation versions accompany the study schema. Patient splitting precedes preprocessing and model fitting, as specified in [EVALUATION_PROTOCOL.md](EVALUATION_PROTOCOL.md).

[Figure 2](../assets/figures/input-contract.svg) maps these public interfaces. Source ultrasound studies, private split manifests and trained checkpoints are outside the current public package.
