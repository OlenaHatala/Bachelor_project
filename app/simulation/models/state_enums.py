from enum import Enum

class SingleSourceState(Enum):
    SOURCE = 0
    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3

SINGLE_STATE2COLOR = {
    SingleSourceState.SOURCE: "red",
    SingleSourceState.SUSCEPTIBLE: "lightsteelblue",
    SingleSourceState.INFECTED: "darkorange",
    SingleSourceState.RECOVERED: "green"
}

SINGLE_STATE_LABELS = {
    SingleSourceState.SUSCEPTIBLE: "Вразливі",
    SingleSourceState.INFECTED: "Інфіковані",
    SingleSourceState.RECOVERED: "Здорові",
    SingleSourceState.SOURCE: "Джерела дезінформації"
}


class AntagonisticState(Enum):
    SOURCE_A = 0
    SOURCE_B = 1
    SUSCEPTIBLE = 2
    INFECTED_A = 3
    INFECTED_B = 4
    RECOVERED = 5

ANTAGONISTIC_STATE2COLOR = {
    AntagonisticState.SOURCE_A: "#f00202", 
    AntagonisticState.SOURCE_B: "#020af0", 
    AntagonisticState.SUSCEPTIBLE: "#bdbdbd",
    AntagonisticState.INFECTED_A: "#f09595",
    AntagonisticState.INFECTED_B: "#959cf0",
    AntagonisticState.RECOVERED: "green"
}

ANTAGONISTIC_STATE_LABELS = {
    AntagonisticState.SOURCE_A: "Джерела дезінформації (A)",
    AntagonisticState.SOURCE_B: "Джерела спростувань (B)",
    AntagonisticState.SUSCEPTIBLE: "Вразливі до впливу",
    AntagonisticState.INFECTED_A: "Інфіковані дезінформацією",
    AntagonisticState.INFECTED_B: "Інфіковані спростуванням",
    AntagonisticState.RECOVERED: "Здорові"
}