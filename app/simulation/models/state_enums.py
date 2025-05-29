from enum import Enum

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
