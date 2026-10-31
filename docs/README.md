# Documentation

Technical notes for the AMTDAN research-preview repository.

| Document | Purpose |
|:---|:---|
| [Figure sources](FIGURES.md) | Links method diagrams and analytical plots to editable assets, rendering code and source values |
| [Model card](MODEL_CARD.md) | Summarizes intended use, current scope, limitations, and privacy boundary |
| [Data interface](DATA_INTERFACE.md) | Defines multimodal examination records and the 17-task label registry |
| [Experiment record](EXPERIMENT_RECORD.md) | Captures module, loss, split, and environment settings |
| [Evaluation protocol](EVALUATION_PROTOCOL.md) | Defines patient-level partitioning and minimum reporting |
| [Artifact manifest](ARTIFACT_MANIFEST.md) | Links schemas, withheld models, evaluation tables, and public figures |
| [Failure analysis](FAILURE_ANALYSIS.md) | Reviews modality, quality, ordinal, domain, and imbalance failures |
| [Release scope](RELEASE_SCOPE.md) | Defines public artifacts, exclusions, and future release gates |
| [Release checklist](RELEASE_CHECKLIST.md) | Verifies preview claims, governance, privacy, and task-level evidence |

## Recommended order

Start with the [model architecture](../README.md#architecture), [public input contract](DATA_INTERFACE.md) and [utility package](../README.md#public-utility-layer). The evaluation protocol defines the reporting design, and the figure catalogue links the diagrams and analytical plot to their sources.
