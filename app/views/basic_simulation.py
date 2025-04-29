import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random 
from simulation.generators.basic_generator import get_available_generators

# st.write("# First page")

st.title("Базова симуляція поширення інформації")

available_generators = get_available_generators()
graph_type = st.selectbox("Оберіть тип графа", list(available_generators.keys()))

with st.form("graph_parameters"):
    n = st.number_input("Кількість вузлів", min_value=1, value=20)

    if graph_type in ["Fast GNP Random Graph", "GNP Random Graph"]:
        p = st.slider("Ймовірність з'єднання", min_value=0.0, max_value=1.0, value=0.2)
        params = (n, p)
    elif graph_type == "Dense GNM Random Graph":  # 🛠️ виправив тут
        m = st.slider("Кількість ребер", min_value=0, max_value=n*(n-1)//2, value=0)
        params = (n, m)
    elif graph_type == "Barabasi-Albert Graph":
        m = st.slider("Кількість підключень нового вузла", min_value=1, max_value=n-1, value=1)
        params = (n, m)
    elif graph_type == "Scale-Free Graph": 
        params = (n,)

    submitted = st.form_submit_button("Згенерувати мережу")


if submitted:
    generator_func = available_generators[graph_type]
    G = generator_func(*params)

    pos = nx.spring_layout(G, seed=42)
    node_colors = ["lightsteelblue"] * len(G.nodes)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edgecolors="black", node_size=500)
    st.pyplot(plt.gcf())
    plt.clf()

    st.session_state.graph = G