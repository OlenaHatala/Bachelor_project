import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import time
import random
import copy


from simulation.generators.basic_generator import GraphGeneratorRegistry
from simulation.models.basic_initializer import BasicSimulationModel, State, STATE2COLOR, plot_state_dynamics, plot_pie_chart, visualize_graph, update_state

# st.set_page_config(page_title="Симуляція поширення у графі", layout="wide")
st.set_page_config(page_title="Симуляція поширення у графі", layout="centered")

st.title("Симуляція поширення у графі")


if "graph" not in st.session_state:
    st.session_state.graph = None
if "simulation_configured" not in st.session_state:
    st.session_state.simulation_configured = False
if "simulation_parameters" not in st.session_state:
    st.session_state.simulation_parameters = None
    

registry = GraphGeneratorRegistry()
graph_type = st.selectbox("Оберіть тип графу", registry.list_generators())


with st.form("graph_parameters"):
    n = st.number_input("Кількість вузлів", min_value=1, value=10)

    if graph_type in ["Fast GNP Random Graph", "GNP Random Graph"]:
        p = st.slider("Ймовірність з'єднання", min_value=0.0, max_value=1.0, value=0.1)
        params = (n, p)
    # elif graph_type == "Dense GNM Random Graph":
    #     m = st.slider("Кількість ребер", min_value=0, max_value=n*(n-1)//2, value=0)
    #     params = (n, m)
    elif graph_type == "Barabasi-Albert Graph":
        m = st.slider("Кількість підключень нового вузла", min_value=1, max_value=n-1, value=1)
        params = (n, m)
    elif graph_type == "Scale-Free Graph":
        params = (n,)
    else:
        params = (n,)

    submitted = st.form_submit_button("Згенерувати мережу")


if submitted:
    generate_func = registry.get_generator(graph_type)
    if generate_func is not None:
        G = generate_func(*params)
        st.session_state.graph = G
        st.session_state.simulation_configured = False
    else:
        st.error("Не вдалося знайти функцію генерації.")


graph_container = st.empty()
plot_container = st.empty()
col1, col2 = st.columns([7, 3])  

with col1:
    plot_container = st.empty()

with col2:
    pie_chart_container = st.empty()


if st.session_state.graph is not None:
    simulator = BasicSimulationModel(st.session_state.graph, source_nodes=[])
    visualize_graph(simulator.graph, graph_container)

    with st.popover("Налаштування симуляції"):
        G = st.session_state.graph
        num_nodes = G.number_of_nodes()

        num_sources = st.number_input(
            "Кількість джерел (source)",
            min_value=1,
            max_value=num_nodes,
            key="num_sources_input"
        )

        simulation_mode = st.radio(
            "Режим симуляції",
            ["Фіксована кількість ітерацій", "Поки змінюються стани"]
        )

        if simulation_mode == "Фіксована кількість ітерацій":
            num_steps = st.number_input(
                "Кількість ітерацій",
                min_value=1,
                max_value=1000,
                key="num_steps_input"
            )


        if st.button("Зберегти"):
            all_nodes = list(G.nodes)
            selected_sources = random.sample(all_nodes, num_sources)

            simulator = BasicSimulationModel(G, selected_sources)
            G = simulator.initialize()
            visualize_graph(G, graph_container)  

            st.session_state.graph = G
            st.session_state.simulation_configured = True

            st.session_state.simulation_parameters = {
                "num_sources": num_sources,
                "simulation_mode": simulation_mode,
                "num_steps": num_steps,
                "selected_sources": selected_sources,
            }


if st.session_state.get("simulation_configured"):
    if st.button("Почати симуляцію"):
        sim_params = st.session_state.simulation_parameters
        sources = sim_params["selected_sources"]
        steps = sim_params["num_steps"] if sim_params["simulation_mode"] == "Фіксована кількість ітерацій" else 100
        
        graph = st.session_state.graph

        state_counts = {state: [] for state in State}

        for step in range(steps):
            graph_copy = copy.deepcopy(graph)

            for node in graph.nodes:

                old_state =  graph_copy.nodes[node]["state"]  # запам’ятовуємо початковий стан
                update_state(graph, graph_copy, node)
                new_state = graph_copy.nodes[node]["state"]       # майбутній стан

            for node in graph.nodes:
                graph.nodes[node]["state"] = graph_copy.nodes[node]["state"]
        

            all_states = [graph.nodes[n]["state"] for n in graph.nodes]
            for state in State:
                state_counts[state].append(all_states.count(state))


            state_count_current = {state: all_states.count(state) for state in State}
            for state in State:
                state_counts[state].append(state_count_current[state])

            with graph_container:
                st.markdown(f'#### Крок {step}')
                visualize_graph(simulator.graph, st)

            with plot_container:
                # st.markdown("#### 📈 Графік динаміки")
                plot_state_dynamics(state_counts, st, steps)

            with pie_chart_container:
                # st.markdown("#### 🥧 Pie Chart")
                plot_pie_chart(state_count_current, st)

            time.sleep(2)
