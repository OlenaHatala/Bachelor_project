import networkx as nx
import random
from enum import Enum

class RemainingNodeStrategy(Enum):
    RANDOM = "Додати до кластерів випадково"
    SEPARATE = "Залишити окремо"


class FlexibleGraphBuilder:
    def __init__(self, total_nodes: int):
        self.total_nodes = total_nodes
        self.graph = nx.DiGraph()

    def build_flat_graph(self, connection_prob: float):
        self.graph = nx.gnp_random_graph(self.total_nodes, connection_prob, directed=True)
        return self.graph

    def build_clustered_graph(
        self,
        cluster_sizes: list[int],
        cluster_probs: list[float],
        intercluster_prob: float = 0.05,
        remaining_strategy: RemainingNodeStrategy = RemainingNodeStrategy.RANDOM,
        external_prob: float = 0.1
    ):
        self.graph.clear()
        current_node = 0
        cluster_nodes = []

        # Створюємо кластери
        for size, prob in zip(cluster_sizes, cluster_probs):
            nodes = list(range(current_node, current_node + size))
            self.graph.add_nodes_from(nodes)
            for i in nodes:
                for j in nodes:
                    if i != j and random.random() < prob:
                        self.graph.add_edge(i, j)
            cluster_nodes.append(nodes)
            current_node += size

        all_nodes = set(range(self.total_nodes))
        assigned_nodes = set(sum(cluster_nodes, []))
        remaining_nodes = list(all_nodes - assigned_nodes)

        # Додаємо залишкові вузли
        if remaining_strategy == RemainingNodeStrategy.RANDOM:
            for node in remaining_nodes:
                self.graph.add_node(node)
                cluster = random.choice(cluster_nodes)
                for target in cluster:
                    if random.random() < external_prob:
                        self.graph.add_edge(node, target)
                    if random.random() < external_prob:
                        self.graph.add_edge(target, node)
        elif remaining_strategy == RemainingNodeStrategy.SEPARATE:
            for i in range(len(remaining_nodes)):
                for j in range(len(remaining_nodes)):
                    if i != j and random.random() < external_prob:
                        self.graph.add_edge(remaining_nodes[i], remaining_nodes[j])

        # Додаємо міжкластерні зв'язки
        for i in range(len(cluster_nodes)):
            for j in range(i + 1, len(cluster_nodes)):
                for node_i in cluster_nodes[i]:
                    for node_j in cluster_nodes[j]:
                        if random.random() < intercluster_prob:
                            self.graph.add_edge(node_i, node_j)
                        if random.random() < intercluster_prob:
                            self.graph.add_edge(node_j, node_i)

        return self.graph
