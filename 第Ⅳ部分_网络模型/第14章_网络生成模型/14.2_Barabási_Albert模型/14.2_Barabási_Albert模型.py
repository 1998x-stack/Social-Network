# 14.2 Barabási-Albert模型
"""
Lecture: 第Ⅳ部分 网络模型/第14章 网络生成模型/14.2 Barabási-Albert模型
Content: 14.2 Barabási-Albert模型

优先连接：新节点以与度成正比概率连到已有节点 → 无标度（幂律）度分布。
"""
from __future__ import annotations

import logging
import random
from collections import Counter

import networkx as nx

from netlab import configure, new_figure, save_fig, setup_logging

log = logging.getLogger("14.2")


def barabasi_albert(m0: int, m: int, n: int, seed: int = 42) -> nx.Graph:
    """生成 BA 图：初始 m0 节点完全图，之后每新增节点连 m 条优先连接边。"""
    rng = random.Random(seed)
    G = nx.complete_graph(m0)
    for _ in range(m0, n):
        nodes = list(G.nodes())
        weights = [G.degree(u) for u in nodes]
        chosen, tries = set(), 0
        while len(chosen) < m and tries < 20 * m:
            chosen.add(rng.choices(nodes, weights=weights, k=1)[0])
            tries += 1
        new = len(nodes)
        G.add_node(new)
        for t in chosen:
            G.add_edge(new, t)
    return G


def degree_distribution(G) -> tuple:
    """返回 (度值升序, 对应频率)。"""
    degs = list(dict(G.degree()).values())
    cnt = Counter(degs)
    ks = sorted(cnt)
    return ks, [cnt[k] / len(degs) for k in ks]


def viz(G):
    """度分布 log-log 图，附幂律参考线。"""
    configure()
    ks, freqs = degree_distribution(G)
    fig, ax = new_figure("BA度分布(对数-对数)", "14.2")
    ax.loglog(ks, freqs, "o", label="模拟")
    if len(ks) >= 2:
        ax.loglog([ks[0], ks[-1]], [freqs[0], freqs[-1]], "--",
                  color="gray", label="幂律参考")
    ax.set_xlabel("k")
    ax.set_ylabel("P(k)")
    ax.legend()
    return save_fig(fig, "14.2", "degree")


def main() -> None:
    setup_logging(module="14.2", logfile="outputs/14.2/run.log")
    G = barabasi_albert(5, 2, 1000, seed=42)
    log.info("ba nodes=%s edges=%s connected=%s", G.number_of_nodes(),
             G.number_of_edges(), nx.is_connected(G))
    png = viz(G)
    log.info("figure saved=%s", png)


if __name__ == "__main__":
    main()