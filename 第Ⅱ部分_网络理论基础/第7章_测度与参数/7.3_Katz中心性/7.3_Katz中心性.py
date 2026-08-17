# 7.3 Katz中心性
"""
Lecture: 第Ⅱ部分 网络理论基础/第7章 测度与参数/7.3 Katz中心性
Content: 7.3 Katz中心性

Katz 中心性：x = beta (I - alpha A^T)^-1 1，alpha < 1/最大特征值保证收敛。
"""
from __future__ import annotations

import logging

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from netlab import configure, new_figure, save_fig, setup_logging

log = logging.getLogger("7.3")


def katz_centrality(adj: np.ndarray, alpha: float, beta: float = 1.0) -> np.ndarray:
    """解 (I - alpha*A^T)x = beta*1 得 Katz 中心性（列随机）。"""
    n = adj.shape[0]
    return np.linalg.solve(np.eye(n) - alpha * adj.T, np.full(n, beta))


def normalize(x: np.ndarray) -> np.ndarray:
    """归一化使各分量和为 1。"""
    s = x.sum()
    return x / s if s != 0 else np.zeros_like(x)


def viz(adj: np.ndarray):
    """网络布局图，节点大小∝Katz 中心性。"""
    configure()
    x = normalize(katz_centrality(adj, 0.1))
    G = nx.from_numpy_array(adj)
    fig, ax = new_figure("Katz中心性", "7.3")
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(
        G,
        pos,
        ax=ax,
        node_size=300 + 3500 * x,
        node_color=list(x),
        cmap=plt.cm.viridis,
        with_labels=True,
    )
    return save_fig(fig, "7.3", "katz")


def main() -> None:
    setup_logging(module="7.3", logfile="outputs/7.3/run.log")
    adj = np.array(
        [[0, 1, 1, 0, 0], [1, 0, 1, 1, 0], [1, 1, 0, 0, 1],
         [0, 1, 0, 0, 1], [0, 0, 1, 1, 0]]
    )
    alpha = 0.2
    x = normalize(katz_centrality(adj, alpha))
    log.info("katz alpha=%s values=%s", alpha, x.round(4).tolist())
    png = viz(adj)
    log.info("figure saved=%s", png)


if __name__ == "__main__":
    main()