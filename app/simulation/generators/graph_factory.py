import networkx as nx
import random

class GraphGeneratorFactory:
    def __init__(self):
        self.generators = {
            "Scale-Free Graph": self.generate_scale_free_graph,
            "Small-World Graph": self.generate_small_world_graph,
        }

    def list_generators(self):
        return list(self.generators.keys())

    def get_generator(self, name):
        return self.generators.get(name, None)

    def generate_scale_free_graph(self, n):
        G = nx.scale_free_graph(n)
        edges = [(u, v) for u, v in G.edges() if u != v] 
        directed = nx.DiGraph()
        directed.add_nodes_from(range(n))
        directed.add_edges_from(edges)
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




# class GraphGeneratorFactory:
#     def __init__(self):
#         self.generators = {
#             "Fast GNP Random Graph": self.generate_fast_gnp_random_graph,
#             "Scale-Free Graph": self.generate_scale_free_graph,
#             "GNP Random Graph": self.generate_gnp_random_graph,
#             # "Dense GNM Random Graph": self.generate_dense_gnm_random_graph,
#             "Barabasi-Albert Graph": self.generate_barabasi_albert_graph,
#         }

#     def list_generators(self):
#         return list(self.generators.keys())

#     def get_generator(self, name):
#         return self.generators.get(name, None)

#     def generate_fast_gnp_random_graph(self, n, p):
#         return nx.fast_gnp_random_graph(n, p, directed=True)

#     def generate_scale_free_graph(self, n):
#         G = nx.scale_free_graph(n)
#         return nx.DiGraph(G)

#     def generate_gnp_random_graph(self, n, p):
#         G = nx.gnp_random_graph(n, p)
#         return nx.DiGraph(G)

#     # def generate_dense_gnm_random_graph(self, n, m):
#     #     G = nx.dense_gnm_random_graph(n, m)
#     #     return nx.DiGraph(G)

#     def generate_barabasi_albert_graph(self, n, m):
#         G = nx.barabasi_albert_graph(n, m)
#         return nx.DiGraph(G)

