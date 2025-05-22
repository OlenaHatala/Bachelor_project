from enum import Enum
import numpy as np

class State(Enum):
    SOURCE = 0
    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3

STATE2COLOR = {
    State.SOURCE: "red",
    State.SUSCEPTIBLE: "lightsteelblue",
    State.INFECTED: "darkorange",
    State.RECOVERED: "green"
}

class BasicGraphInitializer:
    def __init__(self, graph, source_node):
        self.graph = graph
        self.source_node = source_node

    def initialize(self):
        for node in self.graph.nodes:
            if node == self.source_node:
                self.graph.nodes[node]["state"] = State.SOURCE
                self.graph.nodes[node]["resistance"] = 0
            else:
                self.graph.nodes[node]["state"] = State.SUSCEPTIBLE
                self.graph.nodes[node]["resistance"] = np.random.random()

        return self.graph
