"""统一绘图辅助：样式预设、图形工厂、保存约定。"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

FONT_FALLBACK = [
    "PingFang SC",
    "Hiragino Sans GB",
    "Noto Sans CJK SC",
    "WenQuanYi Micro Hei",
    "SimHei",
    "sans-serif",
]
OUTPUT_DIR = Path("outputs")


def configure() -> None:
    """应用全局 matplotlib 样式（中文字体、尺寸、dpi、网格）。"""
    matplotlib.rcParams.update(
        {
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "font.family": "sans-serif",
            "font.sans-serif": FONT_FALLBACK,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "figure.autolayout": True,
        }
    )


def new_figure(
    title: str,
    title_key: str = "",
    figsize: tuple[float, float] = (8.0, 5.0),
) -> tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]:
    """创建带统一标题（含节标识）的 figure。"""
    fig, ax = plt.subplots(figsize=figsize)
    suffix = f"  [{title_key}]" if title_key else ""
    fig.suptitle(f"{title}{suffix}", fontsize=12)
    return fig, ax


def save_fig(
    fig,
    section_key: str,
    name: str,
    dpi: int = 300,
    as_pdf: bool = False,
) -> Path:
    """按约定保存图件到 outputs/<section_key>/，返回 PNG 路径。"""
    out_dir = OUTPUT_DIR / section_key
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / f"{name}_{dpi}dpi.png"
    fig.savefig(png, dpi=dpi)
    if as_pdf:
        fig.savefig(out_dir / f"{name}.pdf", dpi=dpi)
    plt.close(fig)
    return png