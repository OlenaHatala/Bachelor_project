import networkx as nx

def generate_fast_gnp_random_graph(n, p):
    return nx.fast_gnp_random_graph(n, p)

def generate_scale_free_graph(n):
    return nx.scale_free_graph(n)

def generate_gnp_random_graph(n, p):
    return nx.gnp_random_graph(n, p)

def generate_dense_gnm_random_graph(n, m):
    return nx.dense_gnm_random_graph(n, m)

def generate_barabasi_albert_graph(n, m):
    return nx.barabasi_albert_graph(n, m)


def get_available_generators():
    return {
        "Fast GNP Random Graph": generate_fast_gnp_random_graph,
        "Scale-Free Graph": generate_scale_free_graph,
        "GNP Random Graph": generate_gnp_random_graph,
        "Dense GNM Random Graph": generate_dense_gnm_random_graph,
        "Barabasi-Albert Graph": generate_barabasi_albert_graph,
    }