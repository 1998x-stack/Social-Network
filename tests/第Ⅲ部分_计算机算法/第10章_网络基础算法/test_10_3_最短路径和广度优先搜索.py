import networkx as nx
import pytest

from tests.conftest import load_section

SEC = load_section(
    "第Ⅲ部分_计算机算法/第10章_网络基础算法/"
    "10.3_最短路径和广度优先搜索/10.3_最短路径和广度优先搜索.py"
)


def test_bfs_distance_matches_networkx(known_graph):
    got = SEC.bfs_distance(known_graph, 0)
    ref = nx.single_source_shortest_path_length(known_graph, 0)
    assert got == ref


def test_shortest_path_valid(known_graph):
    path = SEC.shortest_path(known_graph, 0, 8)
    assert path[0] == 0 and path[-1] == 8
    assert all(known_graph.has_edge(a, b) for a, b in zip(path, path[1:]))


def test_shortest_path_unreachable_raises():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    G.add_node(99)  # 孤立点，不可达
    with pytest.raises(ValueError):
        SEC.shortest_path(G, 0, 99)