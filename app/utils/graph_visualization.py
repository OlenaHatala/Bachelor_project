import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(G, container, step=None, node_colors=None):
    fig, ax = plt.subplots()

    pos = nx.spring_layout(G, seed=42)

    if node_colors is None:
        node_colors = ["lightsteelblue"] * G.number_of_nodes()

    nx.draw(G, pos, node_color=node_colors, edgecolors="black", node_size=500)

    if step is not None:
        plt.title(f"Крок {step}")

    container.pyplot(fig)
    plt.close(fig)
