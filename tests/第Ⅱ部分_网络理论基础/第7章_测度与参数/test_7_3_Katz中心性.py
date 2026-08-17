import networkx as nx
import numpy as np

from tests.conftest import load_section

SEC = load_section(
    "第Ⅱ部分_网络理论基础/第7章_测度与参数/7.3_Katz中心性/7.3_Katz中心性.py"
)


def test_katz_matches_reference(known_graph):
    nodelist = sorted(known_graph.nodes())
    adj = nx.to_numpy_array(known_graph, nodelist=nodelist)
    alpha = 0.1
    got = SEC.katz_centrality(adj, alpha)
    eye = np.eye(adj.shape[0])
    ref = np.linalg.solve(eye - alpha * adj.T, np.full(adj.shape[0], 1.0))
    assert np.allclose(got, ref, atol=1e-6)


def test_normalize_sums_to_one():
    x = np.array([1.0, 2.0, 3.0])
    assert np.allclose(SEC.normalize(x), x / x.sum())