# Figure sources

| Figure | Basis | Downloads |
|:---|:---|:---|
| Study overview | Model modules in the original architecture diagram and README | [SVG](../assets/figures/study-overview.svg) · [PDF](../assets/figures/study-overview.pdf) |
| Detailed method architecture | Four model modules and feature transformations in the original architecture artifact | [SVG](../assets/figures/method-architecture.svg) · [PDF](../assets/figures/method-architecture.pdf) |
| Public input contract | `ExaminationRecord`, `ModalityState`, `TaskSpec` and `TaskRegistry` | [SVG](../assets/figures/input-contract.svg) · [PDF](../assets/figures/input-contract.pdf) |
| Evaluation protocol | Patient partitioning and reporting steps in `EVALUATION_PROTOCOL.md` | [SVG](../assets/figures/evaluation-protocol.svg) · [PDF](../assets/figures/evaluation-protocol.pdf) |
| Modality-gating response | Outputs of `amtdan.models.compute_gate` | [SVG](../assets/figures/fusion-policy.svg) · [PDF](../assets/figures/fusion-policy.pdf) |

The existing [architecture](../assets/architecture.png) and [confusion-matrix panel](../assets/results.png) are retained as the original PNG artifacts.

## Analytical source tables

- [Quality response](../assets/figures/fusion-policy_data_quality.csv): 101 quality values for each of three logit gaps, giving 303 rows.
- [Availability states](../assets/figures/fusion-policy_data_availability.csv): both modalities, visual only and clinical only.

The quality floor is 0.05. The visual logit takes −1, 0 and +1 while the clinical logit is zero. Availability-state weights use equal logits, with visual quality one when both modalities are present. The curves are exact function evaluations; they have no sampling error bars.

Figures use Arial when available, with Liberation Sans and DejaVu Sans as fallbacks. The PDF embeds the selected font, which is recorded in the manifest.

## Regeneration

Run from the repository root:

```bash
python -m pip install -r requirements-figures.txt
python scripts/make_figures.py
```

The default destination is `outputs/figures/`. To regenerate the published vector assets:

```bash
python scripts/make_figures.py --output-dir assets/figures --formats svg pdf
```

The renderer exports editable text in SVG/PDF and 600 dpi PNG when requested. It also saves the analytical tables and [manifest](../assets/figures/manifest.json), including package versions, plotting parameters and source-table SHA-256 hashes. The main source is [`scripts/make_figures.py`](../scripts/make_figures.py), with local layout helpers in [`scripts/figure_style.py`](../scripts/figure_style.py). Rendering dependencies are pinned in [`requirements-figures.txt`](../requirements-figures.txt).
