import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt

from simulation.generators.basic_generator import GraphGeneratorRegistry
from simulation.models.basic_initializer import BasicGraphInitializer, State, STATE2COLOR


st.title("Базова симуляція поширення інформації")

registry = GraphGeneratorRegistry()
graph_type = st.selectbox("Оберіть тип графа", registry.list_generators())

with st.form("graph_parameters"):
    n = st.number_input("Кількість вузлів", min_value=1, value=20)

    if graph_type in ["Fast GNP Random Graph", "GNP Random Graph"]:
        p = st.slider("Ймовірність з'єднання", min_value=0.0, max_value=1.0, value=0.2)
        params = (n, p)
    elif graph_type == "Dense GNM Random Graph":
        m = st.slider("Кількість ребер", min_value=0, max_value=n*(n-1)//2, value=0)
        params = (n, m)
    elif graph_type == "Barabasi-Albert Graph":
        m = st.slider("Кількість підключень нового вузла", min_value=1, max_value=n-1, value=1)
        params = (n, m)
    elif graph_type == "Scale-Free Graph": 
        params = (n,)

    submitted = st.form_submit_button("Згенерувати мережу")

# if submitted:
#     generator_func = registry.get_generator(graph_type)
#     if generator_func is not None:
#         G = generator_func(*params)

#         # Ініціалізація станів графа
#         source_node = 0  # (або можна випадково вибрати)
#         initializer = BasicGraphInitializer(G, source_node)
#         G = initializer.initialize()

#         pos = nx.spring_layout(G, seed=42)
#         node_colors = [STATE2COLOR[G.nodes[n]["state"]] for n in G.nodes]
#         nx.draw(G, pos, node_color=node_colors, edgecolors="black", node_size=500)
#         st.pyplot(plt.gcf())
#         plt.clf()

#         st.session_state.graph = G
#     else:
#         st.error("Не вдалося знайти функцію генерації для вибраного типу графа.")


# --- Побудова графа ---
if submitted:
    generator_func = registry.get_generator(graph_type)
    if generator_func is not None:
        G = generator_func(*params)
        st.session_state.graph = G
        st.session_state.show_config = True
        st.session_state.sim_configured = False
    else:
        st.error("Не вдалося знайти функцію генерації.")

# --- Поповер для налаштування симуляції ---
if st.session_state.get("show_config"):
    with st.popover("Налаштування симуляції"):
        num_nodes = st.session_state.graph.number_of_nodes()
        num_sources = st.number_input("Кількість джерел (source)", min_value=1, max_value=num_nodes, value=1, key="num_sources")

        sim_mode = st.radio("Режим симуляції", ["Фіксована кількість ітерацій", "Поки змінюються стани"], key="sim_mode")

        if sim_mode == "Фіксована кількість ітерацій":
            num_steps = st.number_input("Кількість ітерацій", min_value=1, max_value=1000, value=20, key="num_steps")
        else:
            num_steps = None

        if st.session_state.get("sim_configured") is False:
            if st.button("OK", key="confirm_config"):
                G = st.session_state.graph
                all_nodes = list(G.nodes)
                selected_sources = random.sample(all_nodes, st.session_state.num_sources)
                initializer = BasicGraphInitializer(G, selected_sources)
                G = initializer.initialize()
                st.session_state.graph = G
                st.session_state.sim_configured = True

                # ОНОВЛЕННЯ ВІЗУАЛІЗАЦІЇ ГРАФА ТУТ
                pos = nx.spring_layout(G, seed=42)
                node_colors = [STATE2COLOR.get(G.nodes[n].get("state", State.SUSCEPTIBLE), "lightsteelblue") for n in G.nodes]
                nx.draw(G, pos, node_color=node_colors, edgecolors="black", node_size=500)
                st.pyplot(plt.gcf())
                plt.clf()


# --- Кнопка початку симуляції ---
if st.session_state.get("sim_configured"):
    st.button("Почати симуляцію")

# --- Візуалізація графа ---
if "graph" in st.session_state:
    G = st.session_state.graph
    pos = nx.spring_layout(G, seed=42)
    node_colors = [STATE2COLOR.get(G.nodes[n].get("state", State.SUSCEPTIBLE), "lightsteelblue") for n in G.nodes]
    nx.draw(G, pos, node_color=node_colors, edgecolors="black", node_size=500)
    st.pyplot(plt.gcf())
    plt.clf()
