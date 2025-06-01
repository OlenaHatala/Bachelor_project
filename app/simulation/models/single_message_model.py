from enum import Enum
import numpy as np
import copy
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import plotly.graph_objects as go


from simulation.models.state_enums import SingleSourceState, SINGLE_STATE2COLOR

class SingleMessageSpreadModel:
    def __init__(self, graph):
        self.graph = graph
        self.source_nodes = []
        self.state_counts = defaultdict(list)  
        self.state_count = {}  

    def initialize(self, source_nodes=None):
        if source_nodes is None:
            self.source_nodes = []
        elif isinstance(source_nodes, int):
            self.source_nodes = [source_nodes]
        else:
            self.source_nodes = list(source_nodes)

        for node in self.graph.nodes:
            if node in self.source_nodes:
                self.graph.nodes[node]["state"] = SingleSourceState.SOURCE
                self.graph.nodes[node]["resistance"] = 0
            else:
                self.graph.nodes[node]["state"] = SingleSourceState.SUSCEPTIBLE
                self.graph.nodes[node]["resistance"] = np.random.random()

        self.update_state_tracking()
        return self.graph


    def get_num_nodes(self):
        return self.graph.number_of_nodes()


    def get_num_sources(self):
        return len(self.source_nodes)


    def step(self):
        graph_copy = self.graph.copy()
        for node in self.graph.nodes:
            self.update_node_state(graph_copy, node)
        for node in self.graph.nodes:
            self.graph.nodes[node]["state"] = graph_copy.nodes[node]["state"]

        self.update_state_tracking()


    def update_node_state(self, graph_copy, node):
        sg = self.graph
        successors = set(sg.neighbors(node))
        predecessors = set(nx.all_neighbors(sg, node)) - successors
        state = sg.nodes[node]["state"]

        if state == SingleSourceState.SOURCE:
            return

        elif state == SingleSourceState.RECOVERED:
            condition = np.random.random()
            if sg.nodes[node]["resistance"] > condition:
                sg.nodes[node]["resistance"] = min(
                    sg.nodes[node]["resistance"] * 2,
                    sg.nodes[node]["resistance"] + np.random.random(),
                    1
                )
            else:
                graph_copy.nodes[node]["state"] = SingleSourceState.SUSCEPTIBLE

        elif state == SingleSourceState.SUSCEPTIBLE:
            source_influenced = SingleSourceState.SOURCE in [graph_copy.nodes[pre]["state"] for pre in predecessors]
            infected_influenced = SingleSourceState.INFECTED in [graph_copy.nodes[pre]["state"] for pre in predecessors]
            if source_influenced or infected_influenced:
                condition = np.random.random()
                if sg.nodes[node]["resistance"] < condition:
                    graph_copy.nodes[node]["state"] = SingleSourceState.INFECTED

        elif state == SingleSourceState.INFECTED:
            condition = np.random.random()
            if sg.nodes[node]["resistance"] > condition:
                graph_copy.nodes[node]["state"] = SingleSourceState.RECOVERED
            else:
                sg.nodes[node]["resistance"] = max(
                    sg.nodes[node]["resistance"] / 2,
                    sg.nodes[node]["resistance"] - np.random.random()
                )


    def update_state_tracking(self):
        """Оновлює історію та поточні підрахунки станів"""
        count = Counter([self.graph.nodes[n]["state"] for n in self.graph.nodes])
        self.state_count = dict(count)  

        for state in SingleSourceState:
            self.state_counts[state].append(count.get(state, 0)) 


    def visualize(self, container, step=None):
        """Візуалізація поточного стану графа"""
        fig, ax = plt.subplots()
        try:
            pos = nx.kamada_kawai_layout(self.graph)
        except:
            pos = nx.spring_layout(self.graph, seed=42)
        node_colors = [
            SINGLE_STATE2COLOR.get(self.graph.nodes[n].get("state", SingleSourceState.SUSCEPTIBLE), "lightsteelblue")
            for n in self.graph.nodes
        ]
        nx.draw(self.graph, pos, node_color=node_colors, edgecolors="black", node_size=500)
        if step is not None:
            plt.title(f"Крок {step}")
        container.pyplot(fig)
        plt.close(fig)