import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import time

# === Налаштування сторінки ===
st.set_page_config(page_title="Симуляція графа", layout="centered")
st.title("Симуляція поширення у графі")

# === Стани ===
class State(Enum):
    SOURCE = 0
    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3

STATE2COLOR = {
    State.SOURCE: "red",
    State.SUSCEPTIBLE: "#5478b3",
    State.INFECTED: "orange",
    State.RECOVERED: "green"
}

# === Функції ===
def initialize_graph(n=6, p=0.3, seed=1):
    G = nx.fast_gnp_random_graph(n=n, p=p, seed=seed, directed=True)
    np.random.seed(seed)
    for node in G.nodes:
        if node == 3 or node == 7:
            G.nodes[node]["state"] = State.SOURCE
            G.nodes[node]["resistance"] = 0.0
        else:
            G.nodes[node]["state"] = State.SUSCEPTIBLE
            G.nodes[node]["resistance"] = np.random.random()
    return G

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

def visualize_graph(sg, pos, container, step=None):
    fig, ax = plt.subplots()
    node_colors = [STATE2COLOR[sg.nodes[node]["state"]] for node in sg.nodes]

    nx.draw_networkx_nodes(sg, pos, ax=ax, node_color=node_colors, edgecolors='black', node_size=500)
    nx.draw_networkx_labels(sg, pos, ax=ax, font_weight='bold')
    nx.draw_networkx_edges(sg, pos, ax=ax, edgelist=sg.edges(), arrowstyle='->', arrowsize=15)

    resistance_labels = {node: f"{sg.nodes[node]['resistance']:.2f}" for node in sg.nodes}
    pos_labels = {node: (x, y + 0.12) for node, (x, y) in pos.items()}
    nx.draw_networkx_labels(sg, pos_labels, ax=ax, labels=resistance_labels, font_size=9, font_color='grey')

    if step is not None:
        plt.title(f"Крок {step}")
    container.pyplot(fig)
    plt.close(fig)  # ✅ ЗАКРИВАЄМО, щоб не накопичувались фігури

def plot_state_dynamics(state_counts, container, total_steps):
    fig, ax = plt.subplots()
    for state, counts in state_counts.items():
        ax.plot(counts, label=state.name, color=STATE2COLOR[state], linewidth=2)

    ax.set_xlim(0, total_steps - 1)  # 🔒 фіксований діапазон по осі X
    ax.set_xlabel("Крок")
    ax.set_ylabel("Кількість вузлів")
    ax.grid(True)
    ax.legend()
    container.pyplot(fig)
    plt.close(fig)  # ✅ ЗАКРИВАЄМО, щоб уникнути витоку пам’яті

# === Параметри користувача ===
num_nodes = st.slider("Кількість вузлів у графі", 3, 20, 8)
probability = st.slider("Ймовірність з'єднання", 0.1, 1.0, 0.3)
steps = st.slider("Кількість кроків симуляції", 1, 50, 15)
delay = st.slider("Затримка між кроками (секунди)", 1, 10, 2)

if st.button("Запустити симуляцію"):
    sg = initialize_graph(n=num_nodes, p=probability)
    pos = nx.spring_layout(sg, seed=5)

    graph_container = st.empty()
    plot_container = st.empty()

    state_counts = {state: [] for state in State}

    for step in range(steps):
        sg_copy = sg.copy()
        for node in sg.nodes:
            update_state(sg, sg_copy, node)
        for node in sg.nodes:
            sg.nodes[node]["state"] = sg_copy.nodes[node]["state"]

        # 📊 Підрахунок станів
        all_states = [sg.nodes[n]["state"] for n in sg.nodes]
        for state in State:
            state_counts[state].append(all_states.count(state))

        # 🖼️ Граф
        with graph_container:
            st.markdown(f"### Крок {step}")
            visualize_graph(sg, pos, st)

        # 📈 Графік динаміки
        with plot_container:
            plot_state_dynamics(state_counts, st, steps)

        time.sleep(delay)
