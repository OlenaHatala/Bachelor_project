import streamlit as st
import random
import matplotlib.pyplot as plt

st.write("# Simulation of Disinformation Spread")

# Опис класів та логіки симуляції
class User:
    def __init__(self, id, influence=0, state="susceptible"):
        self.id = id
        self.state = state
        self.influence = influence  # Вплив користувача (наприклад, кількість підписників)

    def update_state(self, infected_neighbors, government_influence):
        # Ймовірність зараження залежить від кількості інфікованих сусідів та урядового впливу
        infection_prob = sum(1 for n in infected_neighbors) / len(infected_neighbors) if infected_neighbors else 0
        infection_prob *= self.influence  # Вплив користувача
        infection_prob *= (1 - government_influence)  # Вплив уряду (зменшує ймовірність)

        # Заражається чи ні?
        if random.random() < infection_prob:
            self.state = "infected"
        return self.state

class Government:
    def __init__(self, effectiveness):
        self.effectiveness = effectiveness  # Вплив уряду (від 0 до 1)

    def apply_influence(self):
        return self.effectiveness

class Simulation:
    def __init__(self, users, government, connections):
        self.users = users  # Список користувачів
        self.government = government  # Вплив уряду
        self.connections = connections  # Зв'язки між користувачами
        self.history = {'infected': [], 'susceptible': []}  # Історія статистики для графіків

    def run_step(self):
        for user in self.users:
            # Збираємо сусідів користувача (які є інфікованими)
            infected_neighbors = [self.users[neighbor_id] for neighbor_id in self.connections[user.id] if self.users[neighbor_id].state == "infected"]
            user.update_state(infected_neighbors, self.government.apply_influence())

    def simulate(self, steps):
        for step in range(steps):
            self.run_step()
            self.collect_statistics(step)

    def collect_statistics(self, step):
        infected_count = sum(1 for user in self.users if user.state == "infected")
        susceptible_count = sum(1 for user in self.users if user.state == "susceptible")
        
        # Зберігаємо статистику для графіків
        self.history['infected'].append(infected_count)
        self.history['susceptible'].append(susceptible_count)
        
        # Виведення статистики в Streamlit
        st.write(f"**Step {step + 1}:**")
        st.write(f"Infected: {infected_count}, Susceptible: {susceptible_count}")
        
    def plot_statistics(self):
        # Відображення графіків змін
        fig, ax = plt.subplots()
        ax.plot(self.history['infected'], label='Infected', color='darkorange')
        ax.plot(self.history['susceptible'], label='Susceptible', color='lightsteelblue')
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Number of Users')
        ax.legend()
        st.pyplot(fig)

# Ініціалізація параметрів
num_users = st.slider("Number of users", 5, 50, 10)
gov_effectiveness = st.slider("Government Effectiveness", 0.0, 1.0, 0.2)
steps = st.slider("Number of simulation steps", 1, 20, 10)

# Генерація користувачів з випадковим впливом
users = [User(id=i, influence=random.uniform(0.1, 1.0)) for i in range(num_users)]
government = Government(effectiveness=gov_effectiveness)

# Зв'язки між користувачами (по 3 випадкових сусіда для кожного користувача)
connections = {i: [random.randint(0, num_users - 1) for _ in range(3)] for i in range(num_users)}

# Ініціалізація симуляції
simulation = Simulation(users, government, connections)

# Запуск симуляції
simulate_btn = st.button("Start Simulation")

if simulate_btn:
    simulation.simulate(steps)  # Запускаємо симуляцію
    simulation.plot_statistics()  # Виводимо графік статистики
