import networkx as nx
import numpy as np
import pytest

from tests.conftest import load_section

SEC = load_section(
    "第Ⅱ部分_网络理论基础/第6章_网络的数学基础/6.13_图拉普拉斯矩阵/6.13_图拉普拉斯矩阵.py"
)


def test_laplacian_matches_networkx(known_graph):
    nl = sorted(known_graph.nodes())
    adj = nx.to_numpy_array(known_graph, nodelist=nl)
    ref = nx.laplacian_matrix(known_graph, nodelist=nl).toarray()
    assert np.allclose(SEC.laplacian(adj), ref)


def test_row_sum_zero_and_symmetry(known_graph):
    nl = sorted(known_graph.nodes())
    adj = nx.to_numpy_array(known_graph, nodelist=nl)
    L = SEC.laplacian(adj)
    assert np.allclose(L @ np.ones(L.shape[0]), 0)
    assert np.allclose(L, L.T)


def test_fiedler_single_edge():
    L = SEC.laplacian(np.array([[0, 1], [1, 0]]))
    assert SEC.fiedler(np.linalg.eigvalsh(L)) == pytest.approx(2.0)