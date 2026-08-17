import networkx as nx

from netlab import adjacency_matrix, degree_sequence


def test_adjacency_matrix_matches_networkx():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0)])
    got = adjacency_matrix(G)
    expect = nx.to_numpy_array(G, nodelist=[0, 1, 2])
    assert got.shape == (3, 3)
    assert (got == expect).all()


def test_degree_sequence():
    G = nx.path_graph(4)
    assert degree_sequence(G) == [1, 2, 2, 1]


def test_tolerance_positive():
    import netlab.graph_utils as gu

    assert gu.reference_tolerance() > 0