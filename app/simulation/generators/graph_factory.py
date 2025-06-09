import networkx as nx
import random

class GraphGeneratorFactory:
    def __init__(self):
        self.generators = {
            "Безмасштабний граф": self.generate_scale_free_graph,
            "Малосвітовий граф": self.generate_small_world_graph,
        }

    def list_generators(self):
        return list(self.generators.keys())

    def get_generator(self, name):
        return self.generators.get(name, None)

    def generate_scale_free_graph(self, n):
        m = max(1, min(n - 1, 2))  
        G = nx.barabasi_albert_graph(n, m)
        directed = nx.DiGraph()
        directed.add_nodes_from(G.nodes())
        directed.add_edges_from(G.edges())
        return directed


    def generate_small_world_graph(self, n, k=4, p=0.1):
        undirected = nx.watts_strogatz_graph(n, k, p)
        directed = nx.DiGraph()
        directed.add_nodes_from(undirected.nodes)
        for u, v in undirected.edges:
            if u != v:  
                if random.random() < 0.5:
                    directed.add_edge(u, v)
                else:
                    directed.add_edge(v, u)
        return directed