import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

def create_graph(num_nodes):
    G = nx.erdos_renyi_graph(num_nodes, 0.1) 
    return G

def simulate_spread(G, start_node, steps=5):
    infected = [start_node]
    for _ in range(steps):
        new_infected = []
        for node in infected:
            neighbors = list(G.neighbors(node))
            for neighbor in neighbors:
                if neighbor not in infected and random.random() < 0.2:  # 20% шанс поширення
                    new_infected.append(neighbor)
        infected.extend(new_infected)
        infected = list(set(infected))
    return infected

st.title("Симуляція поширення дезінформації у соціальних мережах")

num_nodes = st.slider("Кількість користувачів (вузлів)", 10, 100, 50)
steps = st.slider("Кількість кроків поширення", 1, 10, 5)
start_node = st.slider("Стартовий користувач", 0, num_nodes-1, 0)

G = create_graph(num_nodes)
st.write(f"Граф з {num_nodes} користувачами та зв'язками між ними.")

infected_nodes = simulate_spread(G, start_node, steps)

plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)  # Розташування вузлів
nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue')
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=10)

nx.draw_networkx_nodes(G, pos, nodelist=infected_nodes, node_size=300, node_color='red')

plt.title("Граф поширення дезінформації")
st.pyplot(plt)

