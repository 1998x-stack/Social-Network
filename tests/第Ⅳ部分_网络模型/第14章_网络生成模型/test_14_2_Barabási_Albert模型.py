import networkx as nx

from tests.conftest import load_section

SEC = load_section(
    "第Ⅳ部分_网络模型/第14章_网络生成模型/14.2_Barabási_Albert模型/14.2_Barabási_Albert模型.py"
)


def test_ba_connected_and_size():
    G = SEC.barabasi_albert(5, 2, 200, seed=1)
    assert G.number_of_nodes() == 200
    assert nx.is_connected(G)


def test_ba_degree_sum_even():
    G = SEC.barabasi_albert(3, 2, 50, seed=2)
    assert sum(dict(G.degree()).values()) % 2 == 0


def test_degree_distribution_normalized():
    ks, freqs = SEC.degree_distribution(nx.path_graph(4))
    assert sum(freqs) == 1.0