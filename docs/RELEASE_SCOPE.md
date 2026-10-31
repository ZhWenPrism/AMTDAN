# Release scope

AMTDAN is maintained as a research preview with a public utility package.

## Public contents

| Artifact | Location |
|:---|:---|
| Model overview and reported aggregate values | `README.md` |
| Original architecture and confusion-matrix figures | `assets/architecture.png`, `assets/results.png` |
| Method, interface, protocol and gating figures | `assets/figures/` |
| Examination and task contracts | `amtdan/datasets/schema.py` |
| Modality weights and embedding fusion | `amtdan/models/fusion.py` |
| Ordinal metrics and calibration error | `amtdan/evaluation/metrics.py` |
| Utility regression tests | `tests/unit/` |
| Figure renderer and analytical tables | `scripts/make_figures.py`, `assets/figures/*_data*.csv` |

## Full implementation release

The multi-scale visual encoder, learned spatial attention, cardiac GCN, Transformer and training pipeline remain part of the model design. Their complete experimental implementation and trained weights are pending release.

Clinical images, patient-level records and private split manifests are outside the current public artifact.

## Release records

A full experimental release is linked to the task registry, model configuration, patient split and task-level evaluation tables described in [ARTIFACT_MANIFEST.md](ARTIFACT_MANIFEST.md). The current figure sources are listed in [FIGURES.md](FIGURES.md).
