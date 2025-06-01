import numpy as np
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import networkx as nx

from simulation.models.state_enums import AntagonisticState, ANTAGONISTIC_STATE2COLOR

class AntagonisticSpreadModel:
    def __init__(self, graph):
        self.graph = graph
        self.sources_nodes_A = []
        self.sources_nodes_B = []
        self.state_counts = defaultdict(list)
        self.state_count = {}

    def initialize(self, sources_A=None, sources_B=None):
        if sources_A is None:
            self.sources_nodes_A = []
        elif isinstance(sources_A, int):
            self.sources_nodes_A = [sources_A]
        else:
            self.sources_nodes_A = list(sources_A)

        if sources_B is None:
            self.sources_nodes_B = []
        elif isinstance(sources_B, int):
            self.sources_nodes_B = [sources_B]
        else:
            self.sources_nodes_B = list(sources_B)

        for node in self.graph.nodes:
            if node in self.sources_nodes_A:
                self.graph.nodes[node]["state"] = AntagonisticState.SOURCE_A
                self.graph.nodes[node]["resistance"] = 0
            elif node in self.sources_nodes_B:
                self.graph.nodes[node]["state"] = AntagonisticState.SOURCE_B
                self.graph.nodes[node]["resistance"] = 0
            else:
                self.graph.nodes[node]["state"] = AntagonisticState.SUSCEPTIBLE
                self.graph.nodes[node]["resistance"] = np.random.random()

            trust_a = np.random.uniform(0.3, 0.7)
            self.graph.nodes[node]["trust_A"] = trust_a
            self.graph.nodes[node]["trust_B"] = 1 - trust_a

        self.update_state_tracking()
        return self.graph


    def get_num_nodes(self):
        return self.graph.number_of_nodes()


    def update_state_tracking(self):
        """Оновлює історію та поточні підрахунки станів"""
        count = Counter([self.graph.nodes[n]["state"] for n in self.graph.nodes])
        self.state_count = dict(count)

        for state in AntagonisticState:
            self.state_counts[state].append(count.get(state, 0))



    def step(self):
        graph_copy = self.graph.copy()
        for node in self.graph.nodes:
            self.update_node_state(graph_copy, node)

        # Застосовуємо нові стани
        for node in self.graph.nodes:
            self.graph.nodes[node]["state"] = graph_copy.nodes[node]["state"]

        self.update_state_tracking()


    def update_node_state(self, graph_copy, node):
        sg = self.graph
        state = sg.nodes[node]["state"]

        if state in [AntagonisticState.SOURCE_A, AntagonisticState.SOURCE_B]:
            return

        elif state == AntagonisticState.SUSCEPTIBLE:
            neighbors = set(sg.predecessors(node)) if sg.is_directed() else set(sg.neighbors(node))
            neighbor_states = [graph_copy.nodes[n]["state"] for n in neighbors]

            inf_A = any(s in [AntagonisticState.SOURCE_A, AntagonisticState.INFECTED_A] for s in neighbor_states)
            inf_B = any(s in [AntagonisticState.SOURCE_B, AntagonisticState.INFECTED_B] for s in neighbor_states)

            trust_a = sg.nodes[node]["trust_A"]
            trust_b = sg.nodes[node]["trust_B"]

            if inf_A and not inf_B:
                if trust_a > np.random.random():
                    graph_copy.nodes[node]["state"] = AntagonisticState.INFECTED_A

            elif inf_B and not inf_A:
                if trust_b > np.random.random():
                    graph_copy.nodes[node]["state"] = AntagonisticState.INFECTED_B

            elif inf_A and inf_B:
                # обираємо сторону залежно від довіри
                if trust_a > trust_b and trust_a > np.random.random():
                    graph_copy.nodes[node]["state"] = AntagonisticState.INFECTED_A
                elif trust_b >= trust_a and trust_b > np.random.random():
                    graph_copy.nodes[node]["state"] = AntagonisticState.INFECTED_B

        elif state in [AntagonisticState.INFECTED_A, AntagonisticState.INFECTED_B]:
            if sg.nodes[node]["resistance"] > np.random.random():
                graph_copy.nodes[node]["state"] = AntagonisticState.RECOVERED
            else:
                sg.nodes[node]["resistance"] = max(
                    sg.nodes[node]["resistance"] / 2,
                    sg.nodes[node]["resistance"] - np.random.random()
                )

        elif state == AntagonisticState.RECOVERED:
            if sg.nodes[node]["resistance"] > np.random.random():
                sg.nodes[node]["resistance"] = min(
                    sg.nodes[node]["resistance"] + np.random.random(),
                    2 * sg.nodes[node]["resistance"],
                    1
                )
            else:
                graph_copy.nodes[node]["state"] = AntagonisticState.SUSCEPTIBLE


    def visualize(self, container, step=None):
        """Візуалізація поточного стану графа (антагоністична модель)"""
        fig, ax = plt.subplots()
        pos = nx.spring_layout(self.graph, seed=42)

        node_colors = [
            ANTAGONISTIC_STATE2COLOR.get(
                self.graph.nodes[n].get("state", AntagonisticState.SUSCEPTIBLE),
                "#cccccc"
            )
            for n in self.graph.nodes
        ]

        nx.draw(
            self.graph,
            pos,
            node_color=node_colors,
            edgecolors="black",
            node_size=500
        )

        # За бажанням можна ввімкнути підписи вузлів:
        # nx.draw_networkx_labels(self.graph, pos, font_color="black", font_size=10)

        if step is not None:
            plt.title(f"Крок {step}")

        container.pyplot(fig)
        plt.close(fig)
