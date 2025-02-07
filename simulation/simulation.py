import numpy as np
from Bachelor_project.app.utils.constants import State

def change_states(graph, graph_copy, node):
    node_state = graph.nodes[node]["state"]

    if node_state == State.SOURCE:
        return
    
    elif node_state == State.SUSCEPTIBLE:
        predecessor_states = {graph_copy.nodes[pre]["state"] for pre in set(graph.predecessors(node))}

        if {State.SOURCE, State.INFECTED} & predecessor_states:
            if graph.nodes[node]["resistance"] < np.random.random():
                graph_copy.nodes[node]["state"] = State.INFECTED

    elif node_state == State.INFECTED:
        if graph.nodes[node]["resistance"] > np.random.random():
            graph_copy.nodes[node]["state"] = State.RECOVERED
        else:
            graph.nodes[node]["resistance"] = max(graph.nodes[node]["resistance"]/2, graph.nodes[node]["resistance"]-np.random.random())
        
    elif node_state == State.RECOVERED:
        if graph.nodes[node]["resistance"] > np.random.random():
            graph.nodes[node]["resistance"] = min(graph.nodes[node]["resistance"]+np.random.random(), 2*graph.nodes[node]["resistance"], 1)
        else: 
            graph_copy.nodes[node]["state"] = State.SUSCEPTIBLE
