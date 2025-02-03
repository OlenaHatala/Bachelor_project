import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

st.title("Simulation of desinformation spreading")


num_nodes = st.slider("Number of users", 2, 30, 10)
prob_of_connection = st.slider("Probability of connection", min_value=0.0, max_value=1.0, value=0.2)


graph_type = st.radio(label="Choose graph type", 
                      options=["fast_gnp_random_graph", "scale_free_graph", "gnp_random_graph", "dense_gnm_random_graph", "barabasi_albert_graph"],
                      index=1,
                      horizontal=True
                      )

set_steps_num = st.checkbox("Do you want to set number of simulation steps?")
step_num = None

if set_steps_num:
    step_num = st.number_input("Enter number of steps", value=None, placeholder="Type a number...", min_value=1, step=1)


if st.button("Generate graph", type='secondary'):
    fig, ax = plt.subplots()
    graph = nx.fast_gnp_random_graph(n=num_nodes, p=prob_of_connection, seed=1, directed=True)
    position = nx.spring_layout(graph,seed=5)

    nx.draw_networkx_nodes(graph, position, ax=ax)
    nx.draw_networkx_labels(graph, position, ax=ax, font_weight='bold', font_size=10)
    nx.draw_networkx_edges(graph, position, ax=ax, edgelist= graph.edges())

    st.pyplot(fig)
