import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from constants import State, STATE2COLOR

def create_graph(num_nodes, prob_of_connection):
    plt.close()
    
    graph = nx.fast_gnp_random_graph(n=num_nodes, p=prob_of_connection, seed=1, directed=True)
    np.random.seed(1)
    source_node = 3

    for node in graph.nodes:
        if node == source_node:
            graph.nodes[node]["state"] = State.SOURCE
            graph.nodes[node]["resistance"] = 0
        else:
            graph.nodes[node]["state"] = State.SUSCEPTIBLE
            graph.nodes[node]["resistance"] = np.random.random()
    
    return graph

def visualize_graph(gr, step_num=None):
    fig, ax = plt.subplots()
    position = nx.spring_layout(gr, seed=5)

    node_colors = [STATE2COLOR[State(gr.nodes[node]["state"])] for node in gr.nodes]

    nx.draw_networkx_nodes(gr, position, ax=ax, node_color=node_colors, edgecolors="black", node_size=500)
    nx.draw_networkx_labels(gr, position, ax=ax, font_weight='bold')
    nx.draw_networkx_edges(gr, position, ax=ax)

    if step_num is not None:
        plt.title(f"Step {step_num}", fontsize=14, fontweight="bold", color="black")

    st.pyplot(fig)


# Створення функції для малювання графіків кількості вершин в кожному стані
def plot_state_changes(step_counts):
    plt.close()

    fig, ax = plt.subplots()

    # Додати графіки для кожного стану
    ax.plot(range(1, len(step_counts['susceptible']) + 1), step_counts['susceptible'], label='Susceptible', color=STATE2COLOR[State.SUSCEPTIBLE])
    ax.plot(range(1, len(step_counts['infected']) + 1), step_counts['infected'], label='Infected', color=STATE2COLOR[State.INFECTED])
    ax.plot(range(1, len(step_counts['recovered']) + 1), step_counts['recovered'], label='Recovered', color=STATE2COLOR[State.RECOVERED])

    ax.set_xlabel('Simulation Steps')
    ax.set_ylabel('Number of Nodes')
    ax.set_title('State Changes Over Time')
    ax.legend()

    st.pyplot(fig)