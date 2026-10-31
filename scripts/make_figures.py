"""Render AMTDAN method diagrams and the public modality-gating response."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
from pathlib import Path

import figure_style as cp
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "outputs" / "figures"
QUALITY_FLOOR = 0.05
LOGIT_GAPS = (-1.0, 0.0, 1.0)
QUALITY_GRID = np.linspace(0.0, 1.0, 101)
INK = "#23343D"
GREY = "#6D7C84"
BLUE = "#3F6D8C"
TEAL = "#317A72"
GOLD = "#AA7836"
PALE_BLUE = "#EDF3F7"
PALE_TEAL = "#EDF5F2"
PALE_GOLD = "#FBF3E7"

sys.path.insert(0, str(ROOT))
from amtdan.datasets import ModalityState
from amtdan.models import compute_gate


def node(ax, x, y, w, h, title, body="", color=BLUE, fill=PALE_BLUE):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.07",
        facecolor=fill, edgecolor=color, linewidth=1.05, zorder=2,
    ))
    ax.text(x + w / 2, y + h * (0.68 if body else 0.5), title,
            ha="center", va="center", fontsize=11.2, weight="bold", color=INK, zorder=3)
    if body:
        ax.text(x + w / 2, y + h * 0.30, body, ha="center", va="center",
                fontsize=9.5, color=INK, linespacing=1.45, zorder=3)


def arrow(ax, start, end, *, dashed=False):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=12,
        linewidth=1.1, color=GREY, linestyle="--" if dashed else "-",
        shrinkA=4, shrinkB=4, zorder=1,
    ))


def diagram(title, letter, height=4.7):
    page = cp.Page(height, W=11.6)
    page.frame(0.04, 11.56, 0.04, height - 0.04, title, letter)
    ax = page.ax(0.22, 0.58, 11.16, height - 0.78)
    ax.set(xlim=(0, 11.16), ylim=(0, height - 0.78))
    ax.axis("off")
    return page, ax


def overview():
    page, ax = diagram("AMTDAN: examination-to-severity workflow", "a", 5.0)
    node(ax, 0.06, 2.75, 2.12, 0.90, "Ultrasound", "View + image quality")
    node(ax, 0.06, 0.82, 2.12, 1.00, "Clinical measurements",
         "39 structured variables", TEAL, PALE_TEAL)
    node(ax, 2.88, 2.75, 2.12, 0.90, "Multi-scale encoding", "3 x 3 / 5 x 5 / 7 x 7")
    node(ax, 5.72, 2.75, 2.12, 0.90, "Dynamic attention", "Image-quality modulation")
    node(ax, 5.72, 0.72, 2.12, 1.15, "Cardiac-region graph",
         "Graph propagation\n+ clinical embedding", TEAL, PALE_TEAL)
    node(ax, 8.55, 2.55, 2.48, 1.15, "Global integration",
         "Transformer\n+ task-specific heads", GOLD, PALE_GOLD)
    node(ax, 8.55, 0.72, 2.48, 1.15, "Severity probabilities",
         "17 conditions\n5 ordered grades per task", GOLD, PALE_GOLD)
    for start, end in [
        ((2.18, 3.20), (2.88, 3.20)), ((5.00, 3.20), (5.72, 3.20)),
        ((6.78, 2.75), (6.78, 1.87)), ((2.18, 1.32), (5.72, 1.32)),
        ((7.84, 1.32), (8.55, 3.12)), ((9.79, 2.55), (9.79, 1.87)),
    ]:
        arrow(ax, start, end)
    ax.text(3.93, 1.60, "Feature embedding\nand dimension alignment",
            ha="center", va="center", fontsize=9.5, color=GREY, linespacing=1.4)
    return page.fig, None


def method_architecture():
    page = cp.Page(7.9, W=11.6)
    panels = [
        (0.04, 5.72, 0.04, 3.89, "Multi-scale visual encoding", "a"),
        (5.82, 11.56, 0.04, 3.89, "Quality-aware spatial attention", "b"),
        (0.04, 5.72, 3.99, 7.85, "Cardiac graph and clinical alignment", "c"),
        (5.82, 11.56, 3.99, 7.85, "Global integration and ordinal heads", "d"),
    ]
    axes = []
    for left, right, top, bottom, title, letter in panels:
        page.frame(left, right, top, bottom, title, letter)
        ax = page.ax(left + 0.18, top + 0.60, right - left - 0.36, bottom - top - 0.78)
        ax.set(xlim=(0, 5.32), ylim=(0, 3.05))
        ax.axis("off")
        axes.append(ax)
    ax = axes[0]
    node(ax, 0.08, 1.02, 1.25, 1.08, "Ultrasound", "Normalized views")
    for y, kernel in ((0.16, "7 x 7"), (1.20, "5 x 5"), (2.24, "3 x 3")):
        node(ax, 1.86, y, 1.12, 0.68, kernel)
        arrow(ax, (1.33, 1.56), (1.86, y + 0.34))
        arrow(ax, (2.98, y + 0.34), (3.77, 1.56))
    node(ax, 3.77, 1.02, 1.46, 1.08, "Feature map", "Aligned scales")
    ax.text(2.42, 0.02, "Convolution + batch normalization", ha="center", va="center",
            fontsize=8.8, color=GREY)
    ax = axes[1]
    node(ax, 0.14, 1.98, 2.08, 0.90, "Self-attention", "Query / key / value")
    node(ax, 0.14, 0.28, 2.08, 0.90, "Image quality", "q in [0, 1]", TEAL, PALE_TEAL)
    node(ax, 3.00, 1.00, 2.14, 1.32, "Attention map", "q A + (1 - q) / N", GOLD, PALE_GOLD)
    arrow(ax, (2.22, 2.43), (3.00, 1.66))
    arrow(ax, (2.22, 0.73), (3.00, 1.66))
    ax = axes[2]
    node(ax, 0.08, 2.04, 1.62, 0.90, "Region graph", "Anatomical edges", TEAL, PALE_TEAL)
    node(ax, 0.08, 0.22, 1.62, 0.90, "Clinical vector", "39 measurements", TEAL, PALE_TEAL)
    node(ax, 2.22, 2.04, 1.21, 0.90, "GCN", "Normalized\npropagation", TEAL, PALE_TEAL)
    node(ax, 2.22, 0.22, 1.21, 0.90, "Align", "Embedding\n+ projection", TEAL, PALE_TEAL)
    node(ax, 4.04, 1.12, 1.16, 1.03, "Concat", "Graph +\nclinical", GOLD, PALE_GOLD)
    for start, end in [((1.70, 2.49), (2.22, 2.49)), ((1.70, 0.67), (2.22, 0.67)),
                       ((3.43, 2.49), (4.04, 1.64)), ((3.43, 0.67), (4.04, 1.64))]:
        arrow(ax, start, end)
    ax = axes[3]
    node(ax, 0.08, 1.78, 1.30, 1.10, "Tokens", "Position\nencoding", GOLD, PALE_GOLD)
    node(ax, 1.93, 1.78, 1.51, 1.10, "Transformer", "Attention\n+ feed-forward", GOLD, PALE_GOLD)
    node(ax, 4.00, 1.78, 1.22, 1.10, "Heads", "5 logits\nper task", GOLD, PALE_GOLD)
    node(ax, 0.28, 0.18, 4.74, 1.00, "17 task-specific probability vectors", "Condition-wise softmax")
    arrow(ax, (1.38, 2.33), (1.93, 2.33))
    arrow(ax, (3.44, 2.33), (4.00, 2.33))
    arrow(ax, (4.61, 1.78), (4.61, 1.18))
    return page.fig, None



def input_contract():
    page, ax = diagram("Public interfaces: one examination, explicit modality state", "b", 5.2)
    node(ax, 0.10, 0.68, 3.00, 3.14, "ExaminationRecord",
         "patient_id / exam_id / site\nclinical_features: value or None\nseverity_labels: grade or None\nmodality: ModalityState")
    node(ax, 4.03, 2.21, 3.04, 1.61, "ModalityState",
         "visual_available\nclinical_available\nvisual_quality in [0, 1]", TEAL, PALE_TEAL)
    node(ax, 4.03, 0.30, 3.04, 1.32, "Validation",
         "At least one modality available\nFinite features; grades in 0..4", TEAL, PALE_TEAL)
    node(ax, 8.00, 2.21, 3.04, 1.61, "TaskRegistry",
         "17 unique task names\n5 ordered labels per TaskSpec", GOLD, PALE_GOLD)
    node(ax, 8.00, 0.30, 3.04, 1.32, "Stable task identity",
         "Immutable registry and label order\nUnknown grades retained as None", GOLD, PALE_GOLD)
    arrow(ax, (3.10, 3.00), (4.03, 3.00))
    arrow(ax, (5.55, 2.21), (5.55, 1.62))
    arrow(ax, (9.52, 2.21), (9.52, 1.62))
    return page.fig, None


def evaluation_protocol():
    page, ax = diagram("Evaluation protocol: patient-level separation and frozen reporting", "c", 5.0)
    node(ax, 0.05, 1.45, 1.88, 1.12, "Examinations", "Group repeated studies\nby patient")
    node(ax, 2.52, 1.45, 1.90, 1.12, "Patient split", "Freeze partition\nbefore fitting")
    node(ax, 5.05, 2.72, 2.43, 1.15, "Development",
         "Fit preprocessing on training data\nSelect model on validation data", TEAL, PALE_TEAL)
    node(ax, 5.05, 0.34, 2.43, 1.15, "Held-out evaluation",
         "Apply frozen preprocessing\nand selected model", TEAL, PALE_TEAL)
    node(ax, 8.25, 1.18, 2.77, 1.67, "Task-aware report",
         "Precision / recall / F1\nOrdinal distance + kappa\nCalibration + class support", GOLD, PALE_GOLD)
    for start, end in [
        ((1.93, 2.01), (2.52, 2.01)), ((4.42, 2.01), (5.05, 3.29)),
        ((4.42, 2.01), (5.05, 0.91)), ((7.48, 0.91), (8.25, 2.01)),
    ]:
        arrow(ax, start, end)
    arrow(ax, (6.27, 2.72), (6.27, 1.49), dashed=True)
    ax.text(6.54, 2.10, "Freeze pipeline", ha="left", va="center", fontsize=9.4, color=GREY)
    ax.text(9.63, 0.63, "Stratify by site, device,\nquality and modality state",
            ha="center", va="center", fontsize=9.4, color=GREY, linespacing=1.35)
    return page.fig, None


def fusion_policy():
    page = cp.Page(3.45, W=10.9)
    page.frame(0.04, 5.70, 0.04, 3.40, "Quality-dependent visual weight", "d")
    page.frame(5.78, 10.86, 0.04, 3.40, "Modality-availability states", "e")
    ax = page.ax(0.64, 0.64, 4.77, 2.19)
    state_ax = page.ax(6.41, 0.64, 4.11, 2.19)
    records = []
    colors = (GREY, BLUE, TEAL)
    for gap, color, style in zip(LOGIT_GAPS, colors, ("--", "-", "-.")):
        weights = [
            compute_gate(ModalityState(True, True, float(q)),
                         visual_logit=gap, quality_floor=QUALITY_FLOOR)
            for q in QUALITY_GRID
        ]
        visual = [weight.visual for weight in weights]
        ax.plot(QUALITY_GRID, visual, color=color, linestyle=style, linewidth=1.7,
                label=f"Logit gap = {gap:+.0f}")
        for q, weight in zip(QUALITY_GRID, weights):
            records.append({"quality": q, "visual_logit": gap, "clinical_logit": 0.0,
                            "quality_floor": QUALITY_FLOOR,
                            "visual_weight": weight.visual, "clinical_weight": weight.clinical})
    ax.set(xlabel="Visual quality q", ylabel="Visual-gate weight", xlim=(0, 1), ylim=(0, 1))
    ax.set_xticks(np.linspace(0, 1, 6))
    ax.set_yticks(np.linspace(0, 1, 6))
    ax.legend(loc="upper left", frameon=False, fontsize=8.2)
    ax.axvline(QUALITY_FLOOR, color="#9DA8AE", linewidth=0.8, linestyle=":")
    ax.text(0.98, 0.94, "Quality floor = 0.05", transform=ax.transAxes,
            ha="right", va="top", fontsize=8.2, color=GREY)
    states = (("Both\nq = 1", ModalityState(True, True, 1.0)),
              ("Visual\nonly", ModalityState(True, False)),
              ("Clinical\nonly", ModalityState(False, True)))
    resolved = [compute_gate(state) for _, state in states]
    x = np.arange(len(states))
    visual = np.array([weight.visual for weight in resolved])
    clinical = np.array([weight.clinical for weight in resolved])
    state_ax.bar(x, visual, color=PALE_BLUE, edgecolor=BLUE, linewidth=1.1, width=0.62, label="Visual")
    state_ax.bar(x, clinical, bottom=visual, color=PALE_GOLD, edgecolor=GOLD,
                 linewidth=1.1, width=0.62, label="Clinical")
    state_ax.set(xticks=x, xticklabels=[label for label, _ in states],
                 ylabel="Fusion weight", ylim=(0, 1.14))
    state_ax.legend(loc="upper center", ncol=2, frameon=False, fontsize=8.2)
    for i, (v, c) in enumerate(zip(visual, clinical)):
        if v:
            state_ax.text(i, v / 2, f"{v:.1f}", ha="center", va="center", fontsize=9, color=INK)
        if c:
            state_ax.text(i, v + c / 2, f"{c:.1f}", ha="center", va="center", fontsize=9, color=INK)
    quality = pd.DataFrame(records)
    availability = pd.DataFrame([
        {"state": label.replace("\n", " "), "visual_weight": weight.visual,
         "clinical_weight": weight.clinical}
        for (label, _), weight in zip(states, resolved)
    ])
    assert np.allclose(quality.visual_weight + quality.clinical_weight, 1.0)
    print(f"quality-response rows: {len(quality)}; availability states: {len(availability)}; filtered: 0")
    return page.fig, {"quality": quality, "availability": availability}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--formats", nargs="+", choices=("svg", "png", "pdf"),
                        default=("svg", "png", "pdf"))
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    cp.apply_style()
    matplotlib.rcParams.update({"svg.hashsalt": "amtdan-figures-v1", "axes.unicode_minus": False})
    figures = []
    for name, builder in (
        ("study-overview", overview), ("method-architecture", method_architecture),
        ("input-contract", input_contract),
        ("evaluation-protocol", evaluation_protocol), ("fusion-policy", fusion_policy),
    ):
        figure, data = builder()
        report = cp.save_figure(figure, output / name, data=data, script=__file__,
                                formats=tuple(args.formats), dpi=600)
        if report["issues"]:
            raise RuntimeError(f"Figure layout check failed for {name}: {report['issues']}")
        figures.append({"name": name, "exports": [Path(path).name for path in report["files"]
                                                  if not path.endswith("_script.py")],
                        "fonts": report["fonts"], "layout_issues": len(report["issues"])})
    data_files = sorted(output.glob("*_data*.csv"))
    manifest = {
        "renderer": "scripts/make_figures.py",
        "python": platform.python_version(),
        "packages": {name: importlib.metadata.version(name) for name in ("matplotlib", "numpy", "pandas")},
        "style_source": "scripts/figure_style.py",
        "quality_floor": QUALITY_FLOOR, "logit_gaps": list(LOGIT_GAPS),
        "data_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in data_files},
        "figures": figures,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
