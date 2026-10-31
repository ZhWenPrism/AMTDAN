"""Small, portable layout helpers for the AMTDAN figure set."""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.text import Text


def apply_style():
    installed = {font.name for font in font_manager.fontManager.ttflist}
    family = next(name for name in ("Arial", "Liberation Sans", "DejaVu Sans") if name in installed)
    matplotlib.rcParams.update({
        "font.family": family,
        "font.size": 9, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 1.05, "xtick.major.width": 1.05, "ytick.major.width": 1.05,
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "figure.facecolor": "white", "axes.facecolor": "white",
    })


class Page:
    def __init__(self, height, W):
        self.height, self.width = height, W
        self.fig = plt.figure(figsize=(W, height))

    def frame(self, left, right, top, bottom, title, letter):
        x, y = left / self.width, 1 - bottom / self.height
        w, h = (right - left) / self.width, (bottom - top) / self.height
        self.fig.add_artist(Rectangle(
            (x, y), w, h, transform=self.fig.transFigure,
            facecolor="white", edgecolor="#B8B8B8", linewidth=0.75, zorder=-2,
        ))
        band = 0.23
        self.fig.add_artist(FancyBboxPatch(
            ((left + 0.04) / self.width, 1 - (top + band + 0.02) / self.height),
            (right - left - 0.08) / self.width, band / self.height,
            boxstyle="round,pad=0.001,rounding_size=0.005",
            transform=self.fig.transFigure, facecolor="#EAEAEA",
            edgecolor="none", zorder=-1,
        ))
        self.fig.text((left + right) / (2 * self.width),
                      1 - (top + 0.02 + band / 2) / self.height,
                      title, ha="center", va="center", fontsize=9.5, color="#202020")
        self.fig.text((left + 0.10) / self.width,
                      1 - (top + 0.02 + band / 2) / self.height,
                      letter, ha="left", va="center", fontsize=11, weight="bold")

    def ax(self, left, top, width, height):
        return self.fig.add_axes([
            left / self.width, 1 - (top + height) / self.height,
            width / self.width, height / self.height,
        ])


def _check_layout(fig):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    issues = []
    for text in fig.findobj(match=Text):
        if not text.get_visible() or not text.get_text().strip():
            continue
        box = text.get_window_extent(renderer)
        if text.get_fontsize() < 4.5:
            issues.append("text smaller than 4.5 pt")
        tolerance = 3
        if (box.x0 < bounds.x0 - tolerance or box.y0 < bounds.y0 - tolerance
                or box.x1 > bounds.x1 + tolerance or box.y1 > bounds.y1 + tolerance):
            issues.append("text outside figure: " + text.get_text())
    return issues


def save_figure(fig, stem, data=None, script=None, formats=("svg", "pdf", "png"), dpi=600):
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    issues = _check_layout(fig)
    files = []
    for extension in formats:
        target = stem.with_suffix("." + extension)
        fig.savefig(target, dpi=dpi, bbox_inches="tight", pad_inches=0.04)
        files.append(str(target))
    if data is not None:
        for key, table in (data.items() if isinstance(data, dict) else [("values", data)]):
            target = stem.parent / (stem.name + "_data_" + key + ".csv")
            pd.DataFrame(table).to_csv(target, index=False, lineterminator="\n")
            files.append(str(target))
    fonts = []
    if "pdf" in formats:
        raw = stem.with_suffix(".pdf").read_bytes()
        fonts = sorted({re.sub(r"^[A-Z]{6}\+", "", match.decode("latin-1")) for match in
                        re.findall(rb"/BaseFont\s*/([A-Za-z0-9+_.-]+)", raw)})
    plt.close(fig)
    print(f"{stem.name}: {len(issues)} layout issue(s); {len(files)} exported file(s)")
    return {"files": files, "fonts": fonts, "issues": issues}

