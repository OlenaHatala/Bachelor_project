from enum import Enum
import numpy as np
import copy
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt

from simulation.models.state_enums import State, STATE2COLOR

class SingleMessageSpreadModel:
    def __init__(self, graph):
        self.graph = graph
        self.source_nodes = []

    def initialize(self, source_nodes=None):
        if source_nodes is None:
            self.source_nodes = []
        elif isinstance(source_nodes, int):
            self.source_nodes = [source_nodes]
        else:
            self.source_nodes = list(source_nodes)

        for node in self.graph.nodes:
            if node in self.source_nodes:
                self.graph.nodes[node]["state"] = State.SOURCE
                self.graph.nodes[node]["resistance"] = 0
            else:
                self.graph.nodes[node]["state"] = State.SUSCEPTIBLE
                self.graph.nodes[node]["resistance"] = np.random.random()
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


    def update_node_state(self, graph_copy, node):
        sg = self.graph
        successors = set(sg.neighbors(node))
        predecessors = set(nx.all_neighbors(sg, node)) - successors
        state = sg.nodes[node]["state"]

        if state == State.SOURCE:
            return

        elif state == State.RECOVERED:
            condition = np.random.random()
            if sg.nodes[node]["resistance"] > condition:
                sg.nodes[node]["resistance"] = min(
                    sg.nodes[node]["resistance"] * 2,
                    sg.nodes[node]["resistance"] + np.random.random(),
                    1
                )
            else:
                graph_copy.nodes[node]["state"] = State.SUSCEPTIBLE

        elif state == State.SUSCEPTIBLE:
            source_influenced = State.SOURCE in [graph_copy.nodes[pre]["state"] for pre in predecessors]
            infected_influenced = State.INFECTED in [graph_copy.nodes[pre]["state"] for pre in predecessors]
            if source_influenced or infected_influenced:
                condition = np.random.random()
                if sg.nodes[node]["resistance"] < condition:
                    graph_copy.nodes[node]["state"] = State.INFECTED

        elif state == State.INFECTED:
            condition = np.random.random()
            if sg.nodes[node]["resistance"] > condition:
                graph_copy.nodes[node]["state"] = State.RECOVERED
            else:
                sg.nodes[node]["resistance"] = max(
                    sg.nodes[node]["resistance"] / 2,
                    sg.nodes[node]["resistance"] - np.random.random()
                )


    def visualize(self, container, step=None):
        """Візуалізація поточного стану графа"""
        fig, ax = plt.subplots()
        pos = nx.spring_layout(self.graph, seed=42)
        node_colors = [
            STATE2COLOR.get(self.graph.nodes[n].get("state", State.SUSCEPTIBLE), "lightsteelblue")
            for n in self.graph.nodes
        ]
        nx.draw(self.graph, pos, node_color=node_colors, edgecolors="black", node_size=500)
        nx.draw_networkx_labels(self.graph, pos, font_color="black", font_size=10)
        if step is not None:
            plt.title(f"Крок {step}")
        container.pyplot(fig)
        plt.close(fig)




# ----- FOR OLD PAGE -----

def visualize_graph(G, container, step=None):
    fig, ax = plt.subplots()

    pos = nx.spring_layout(G, seed=42)
    node_colors = [
        STATE2COLOR.get(G.nodes[n].get("state", State.SUSCEPTIBLE), "lightsteelblue")
        for n in G.nodes
    ]

    nx.draw(G, pos, node_color=node_colors, edgecolors="black", node_size=500)

    if step is not None:
        plt.title(f"Крок {step}")
    container.pyplot(fig)
    plt.close(fig)  # ✅ ЗАКРИВАЄМО, щоб не накопичувались фігури




def plot_state_dynamics(state_counts, container, total_steps):
    fig, ax = plt.subplots()
    for state, counts in state_counts.items():
        ax.plot(counts, label=state.name, color=STATE2COLOR[state], linewidth=2)

    ax.set_xlim(0, total_steps - 1)  
    ax.set_xlabel("Крок")
    ax.set_ylabel("Кількість вузлів")
    ax.grid(True)
    ax.legend()
    container.pyplot(fig)
    plt.close(fig)  


import matplotlib.pyplot as plt

def autopct_hide_zero(pct):
    return f'{pct:.0f}%' if pct > 0 else ''

def plot_pie_chart(state_count, container):
    sizes = list(state_count.values())
    colors = [STATE2COLOR[state] for state in state_count.keys()]

    fig, ax = plt.subplots(figsize=(2.5, 2.5))  # 🔧 Компактно

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,                       # ❌ Без назв
        autopct=autopct_hide_zero,         # ✅ Свої правила показу
        startangle=90,
        colors=colors,
        textprops=dict(color="black", fontsize=9, weight='bold'),
        wedgeprops=dict(width=0.5)         # 🔘 Бублик
    )

    ax.axis('equal')  # 🔵 Коло
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # 🔧 Без полів

    container.pyplot(fig)
    plt.close(fig)


def update_state(sg, sg_copy, node):
    successors = set(sg.neighbors(node))
    predecessors = set(nx.all_neighbors(sg, node)) - successors
    state = sg.nodes[node]["state"]

    if state == State.SOURCE:
        return

    elif state == State.RECOVERED:
        condition = np.random.random()
        if sg.nodes[node]["resistance"] > condition:
            sg.nodes[node]["resistance"] = min(sg.nodes[node]["resistance"] * 2,
                                               sg.nodes[node]["resistance"] + np.random.random(), 1)
        else:
            sg_copy.nodes[node]["state"] = State.SUSCEPTIBLE

    elif state == State.SUSCEPTIBLE:
        source_influenced = State.SOURCE in [sg_copy.nodes[pre]["state"] for pre in predecessors]
        infected_influenced = State.INFECTED in [sg_copy.nodes[pre]["state"] for pre in predecessors]
        if source_influenced or infected_influenced:
            condition = np.random.random()
            if sg.nodes[node]["resistance"] < condition:
                sg_copy.nodes[node]["state"] = State.INFECTED

    elif state == State.INFECTED:
        condition = np.random.random()
        if sg.nodes[node]["resistance"] > condition:
            sg_copy.nodes[node]["state"] = State.RECOVERED
        else:
            sg.nodes[node]["resistance"] = max(sg.nodes[node]["resistance"] / 2,
                                               sg.nodes[node]["resistance"] - np.random.random())
