import random

def assign_random_sources_from_clusters(cluster_map, source_distribution, outside_sources):
    sources = []

    for i, count in enumerate(source_distribution):
        nodes = cluster_map.get(i, [])
        sources += random.sample(nodes, min(len(nodes), count))

    if (outside_sources is not None and outside_sources > 0):
        outside_nodes = cluster_map.get("around", [])
        sources += random.sample(outside_nodes, min(len(outside_nodes), outside_sources))

    return sources
