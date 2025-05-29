import matplotlib.pyplot as plt
import networkx as nx
import random

def create_custom_clustered_graph():
    total_nodes = int(input("Введіть загальну кількість вузлів: "))
    num_clusters = int(input("Введіть кількість кластерів: "))

    G = nx.Graph()
    node_offset = 0
    cluster_nodes_list = []

    for i in range(num_clusters):
        print(f"\nКластер {i + 1}:")
        cluster_size = int(input(f"  Кількість вузлів у кластері {i + 1}: "))
        connection_prob = float(input(f"  Ймовірність з'єднання у кластері {i + 1} (від 0 до 1): "))

        cluster_nodes = list(range(node_offset, node_offset + cluster_size))
        cluster_nodes_list.append(cluster_nodes)
        node_offset += cluster_size

        G.add_nodes_from(cluster_nodes)

        # Додаємо ребра у кластері
        for u in cluster_nodes:
            for v in cluster_nodes:
                if u < v and random.random() < connection_prob:
                    G.add_edge(u, v)

    remaining_nodes_count = total_nodes - node_offset

    if remaining_nodes_count > 0:
        print(f"\nЗалишилося {remaining_nodes_count} вузлів, які не входять до кластерів.")
        option = input("Додати ці вузли до наявних кластерів випадково (r) чи залишити окремими (o)? (r/o): ").lower()

        remaining_nodes = list(range(node_offset, node_offset + remaining_nodes_count))
        G.add_nodes_from(remaining_nodes)

        if option == 'r':
            for node in remaining_nodes:
                target_cluster = random.choice(cluster_nodes_list)
                target_node = random.choice(target_cluster)
                G.add_edge(node, target_node)

        elif option == 'o':
            ext_connection_prob = float(input("  Введіть ймовірність з'єднання залишкових вузлів з усіма іншими: "))
            for node in remaining_nodes:
                for target_node in G.nodes:
                    if node != target_node and random.random() < ext_connection_prob:
                        G.add_edge(node, target_node)
        else:
            print("⚠️ Невідома опція. Залишкові вузли не були з'єднані.")

    print(f"\n✅ Граф створено. Кількість вузлів: {G.number_of_nodes()}, ребер: {G.number_of_edges()}")
    return G


# Приклад запуску
if __name__ == "__main__":
    graph = create_custom_clustered_graph()
    nx.draw(graph, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500)
    plt.title("Згенерований граф із кластерами")
    plt.show()
