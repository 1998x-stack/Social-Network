# 6.13 图拉普拉斯矩阵
"""
Lecture: 第Ⅱ部分 网络理论基础/第6章 网络的数学基础/6.13 图拉普拉斯矩阵
Content: 6.13 图拉普拉斯矩阵

L = D - A。L·1 = 0；最小特征值 0；第二小特征值（Fiedler）衡量连通性。
"""
from __future__ import annotations

import logging

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from netlab import configure, new_figure, save_fig, setup_logging

log = logging.getLogger("6.13")


def laplacian(adj: np.ndarray) -> np.ndarray:
    """返回 L = D - A（D 为度对角矩阵）。"""
    return np.diag(adj.sum(axis=1)) - adj


def fiedler(evals: np.ndarray) -> float:
    """返回第二小特征值。"""
    return float(np.sort(evals)[1])


def viz(adj: np.ndarray):
    """特征值谱与按 Fiedler 向量着色的布局图。"""
    configure()
    L = laplacian(adj)
    evals = np.linalg.eigvalsh(L)
    fig, ax = new_figure("拉普拉斯特征值谱", "6.13")
    ax.plot(range(len(evals)), evals, "o-")
    ax.set_xlabel("index")
    ax.set_ylabel("λ")
    p1 = save_fig(fig, "6.13", "eigs")

    _, vecs = np.linalg.eigh(L)
    fied = vecs[:, 1]
    G = nx.from_numpy_array(adj)
    fig2, ax2 = new_figure("Fiedler向量着色", "6.13")
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(G, pos, ax=ax2, node_color=list(fied),
                     cmap=plt.cm.coolwarm, with_labels=True)
    p2 = save_fig(fig2, "6.13", "fiedler")
    return p1, p2


def main() -> None:
    setup_logging(module="6.13", logfile="outputs/6.13/run.log")
    adj = np.array([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]])
    L = laplacian(adj)
    evals = np.linalg.eigvalsh(L)
    log.info("laplacian evals=%s fiedler=%s", evals.round(4).tolist(), fiedler(evals))
    p1, p2 = viz(adj)
    log.info("figures saved=%s %s", p1, p2)


if __name__ == "__main__":
    main()