import importlib.util
import sys
from pathlib import Path

import matplotlib
import networkx as nx
import pytest

matplotlib.use("Agg")  # CI/测试无窗口

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def load_section(rel_path: str):
    """按仓库根相对路径加载任意 section（支持中文/带点文件名）。"""
    full = (PROJECT_ROOT / rel_path).resolve()
    if not full.exists():
        raise FileNotFoundError(full)
    spec = importlib.util.spec_from_file_location(full.stem, full)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def known_graph():
    """固定的 9 节点简单无向图，用于确定性测试。"""
    G = nx.Graph()
    G.add_edges_from(
        [
            (0, 1), (1, 2), (2, 3), (3, 0), (0, 4),
            (1, 5), (4, 5), (4, 6), (5, 7), (6, 7), (7, 8),
        ]
    )
    return G


@pytest.fixture
def simple_graph():
    return nx.path_graph(4)