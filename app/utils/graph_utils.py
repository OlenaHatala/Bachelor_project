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


def assign_sources_dual(cluster_map, 
                        source_dist_A, outside_A, 
                        source_dist_B, outside_B, 
                        total_nodes):
    assigned_A = set()
    assigned_B = set()

    def sample_without_overlap(node_pool, count, already_assigned):
        candidates = list(set(node_pool) - already_assigned)
        if len(candidates) < count:
            raise ValueError("Not enough nodes available to sample without overlap.")
        return set(random.sample(candidates, count))

    # Assign sources A from clusters
    for i, count in enumerate(source_dist_A):
        if count > 0:
            assigned_A.update(sample_without_overlap(cluster_map[i], count, assigned_A.union(assigned_B)))

    # Assign sources B from clusters
    for i, count in enumerate(source_dist_B):
        if count > 0:
            assigned_B.update(sample_without_overlap(cluster_map[i], count, assigned_A.union(assigned_B)))

    # Assign A from remaining ("around")
    if outside_A > 0 and "around" in cluster_map:
        assigned_A.update(sample_without_overlap(cluster_map["around"], outside_A, assigned_A.union(assigned_B)))

    # Assign B from remaining ("around")
    if outside_B > 0 and "around" in cluster_map:
        assigned_B.update(sample_without_overlap(cluster_map["around"], outside_B, assigned_A.union(assigned_B)))

    # Final sanity check
    if len(assigned_A.intersection(assigned_B)) > 0:
        raise ValueError("Sources A and B overlap")

    if len(assigned_A.union(assigned_B)) > total_nodes:
        raise ValueError("Total number of assigned sources exceeds node count.")

    return list(assigned_A), list(assigned_B)
