"""共享图工具：邻接矩阵、度序列、参考容差。"""
from __future__ import annotations

import networkx as nx
import numpy as np


def adjacency_matrix(G: nx.Graph) -> np.ndarray:
    """按排序节点顺序返回 float 邻接矩阵。"""
    return nx.to_numpy_array(G, nodelist=sorted(G.nodes()))


def degree_sequence(G: nx.Graph) -> list[int]:
    """按排序节点顺序返回度序列。"""
    order = sorted(G.nodes())
    return [G.degree(n) for n in order]


def reference_tolerance() -> float:
    """参考交叉验证的默认容差。"""
    return 1e-6