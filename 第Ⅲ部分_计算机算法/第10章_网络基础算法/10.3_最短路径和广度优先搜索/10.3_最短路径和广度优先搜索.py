# 10.3 最短路径和广度优先搜索
"""
Lecture: 第Ⅲ部分 计算机算法/第10章 网络基础算法/10.3 最短路径和广度优先搜索
Content: 10.3 最短路径和广度优先搜索

BFS 在无权图上逐层推进求最短距离；由前驱回溯得最短路径。复杂度 O(V+E)。
"""
from __future__ import annotations

import logging

import matplotlib.pyplot as plt
import networkx as nx

from netlab import configure, new_figure, save_fig, setup_logging

log = logging.getLogger("10.3")


def bfs_distance(G, source: int) -> dict:
    """BFS 计算源点到各节点的最短距离（无权图）。"""
    dist = {source: 0}
    frontier = [source]
    while frontier:
        nxt = []
        for u in frontier:
            for v in G.neighbors(u):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    nxt.append(v)
        frontier = nxt
    return dist


def shortest_path(G, source: int, target: int) -> list:
    """用 BFS 前驱回溯返回 source 到 target 的一条最短路径。"""
    if target not in bfs_distance(G, source):
        raise ValueError(f"target {target} 不可达")
    prev = {source: None}
    frontier = [source]
    while frontier:
        nxt = []
        for u in frontier:
            for v in G.neighbors(u):
                if v not in prev:
                    prev[v] = u
                    nxt.append(v)
        frontier = nxt
    path, node = [], target
    while node is not None:
        path.append(node)
        node = prev[node]
    return path[::-1]


def viz(G, source: int, target: int):
    """按距离着色节点并高亮输出最短路径。"""
    configure()
    dist = bfs_distance(G, source)
    fig, ax = new_figure("BFS最短路径", "10.3")
    pos = nx.spring_layout(G, seed=42)
    colors = [dist.get(n, -1) for n in G.nodes()]
    nx.draw_networkx(G, pos, ax=ax, node_color=colors, cmap=plt.cm.turbo,
                     with_labels=True)
    path = shortest_path(G, source, target)
    edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges,
                           edge_color="red", width=3)
    return save_fig(fig, "10.3", "bfs")


def main() -> None:
    setup_logging(module="10.3", logfile="outputs/10.3/run.log")
    G = nx.convert_node_labels_to_integers(nx.grid_2d_graph(3, 5).to_undirected())
    source, target = 0, G.number_of_nodes() - 1
    dist = bfs_distance(G, source)
    log.info("bfs nodes=%s max_dist=%s", G.number_of_nodes(), max(dist.values()))
    path = shortest_path(G, source, target)
    log.info("path=%s len=%s", path, len(path))
    png = viz(G, source, target)
    log.info("figure saved=%s", png)


if __name__ == "__main__":
    main()