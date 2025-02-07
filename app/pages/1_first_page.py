import streamlit as st
import networkx as nx
import time
from app.utils.constants import State
from app.utils.graph_utils import create_graph, plot_state_changes, visualize_graph
from simulation.simulation import change_states

st.title("Simulation of Desinformation Spreading")

num_nodes = st.slider("Number of users", 2, 30, 10)
prob_of_connection = st.slider("Probability of connection", min_value=0.0, max_value=1.0, value=0.2)

set_steps_num = st.checkbox("Do you want to set the number of simulation steps?")
step_num = st.number_input("Enter number of steps", min_value=1, step=1) if set_steps_num else None

graph_type = st.radio(label="Choose graph type", 
                      options=["fast_gnp_random_graph", "scale_free_graph", "gnp_random_graph", "dense_gnm_random_graph", "barabasi_albert_graph"],
                      index=1,
                      horizontal=True
                      )

graph = create_graph(num_nodes, prob_of_connection)

col1, col2 = st.columns(2)
with col1:
    generate_btn = st.button("Generate Graph", type="secondary")
with col2:
    simulate_btn = st.button("Simulate", type="primary", disabled=not generate_btn)

# Контейнер для оновлення графа
graph_placeholder = st.empty()
graph_stats_placeholder = st.empty()

step_counts = {
    'susceptible': [],
    'infected': [],
    'recovered': []
}


if generate_btn:
    with graph_placeholder:
        visualize_graph(graph)

if simulate_btn:
    for step in range(1, (step_num or 2) + 1):
        graph_copy = graph.copy()

        # Оновлення станів на поточному кроці
        for node in graph.nodes:
            change_states(graph, graph_copy, node)
        for node in graph.nodes:
            graph.nodes[node]["state"] = graph_copy.nodes[node]["state"]

        # Збираємо статистику про стани на поточному кроці
        susceptible_count = sum(1 for node in graph.nodes if graph.nodes[node]["state"] == State.SUSCEPTIBLE)
        infected_count = sum(1 for node in graph.nodes if graph.nodes[node]["state"] == State.INFECTED)
        recovered_count = sum(1 for node in graph.nodes if graph.nodes[node]["state"] == State.RECOVERED)

        # Додаємо до списку
        step_counts['susceptible'].append(susceptible_count)
        step_counts['infected'].append(infected_count)
        step_counts['recovered'].append(recovered_count)

        # Оновлюємо граф та графіки
        with graph_placeholder:
            visualize_graph(graph, step_num=step)  # Оновлюємо граф симуляції

        with graph_stats_placeholder:
            plot_state_changes(step_counts)

        time.sleep(1)  # Затримка 1 секунда