import networkx as nx

class GraphGeneratorFactory:
    def __init__(self):
        self.generators = {
            "Fast GNP Random Graph": self.generate_fast_gnp_random_graph,
            "Scale-Free Graph": self.generate_scale_free_graph,
            "GNP Random Graph": self.generate_gnp_random_graph,
            # "Dense GNM Random Graph": self.generate_dense_gnm_random_graph,
            "Barabasi-Albert Graph": self.generate_barabasi_albert_graph,
        }

    def list_generators(self):
        return list(self.generators.keys())

    def get_generator(self, name):
        return self.generators.get(name, None)

    def generate_fast_gnp_random_graph(self, n, p):
        return nx.fast_gnp_random_graph(n, p, directed=True)

    def generate_scale_free_graph(self, n):
        G = nx.scale_free_graph(n)
        return nx.DiGraph(G)

    def generate_gnp_random_graph(self, n, p):
        G = nx.gnp_random_graph(n, p)
        return nx.DiGraph(G)

    # def generate_dense_gnm_random_graph(self, n, m):
    #     G = nx.dense_gnm_random_graph(n, m)
    #     return nx.DiGraph(G)

    def generate_barabasi_albert_graph(self, n, m):
        G = nx.barabasi_albert_graph(n, m)
        return nx.DiGraph(G)
