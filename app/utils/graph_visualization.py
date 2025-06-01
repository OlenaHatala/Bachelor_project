import matplotlib.pyplot as plt
import networkx as nx
from simulation.models.state_enums import SingleSourceState, SINGLE_STATE2COLOR
import plotly.graph_objects as go


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


# def plot_state_dynamics(state_counts, container, total_steps):
#     fig = go.Figure()

#     for state, counts in state_counts.items():
#         fig.add_trace(go.Scatter(
#             x=list(range(len(counts))),
#             y=counts,
#             mode='lines+markers',  # 🔘 лінії + точки
#             name=state.name,
#             line=dict(color=SINGLE_STATE2COLOR[state], width=2),
#             marker=dict(size=6)
#         ))

#     fig.update_layout(
#         title=dict(
#             text="Динаміка станів",
#             x=0.5, 
#             xanchor='center'
#         ),
#         title_automargin=True,
#         xaxis_title="Крок",
#         yaxis_title="Кількість вузлів",
#         xaxis=dict(range=[0, total_steps]),
#         yaxis=dict(rangemode='tozero'),
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#         height=350,
#         margin=dict(l=10, r=10, t=40, b=10)
#     )

#     container.plotly_chart(fig, use_container_width=True)


def plot_state_dynamics(state_counts, container, total_steps, state2color: dict):
    fig = go.Figure()

    for state, counts in state_counts.items():
        color = state2color.get(state, "#999999")  # fallback колір, якщо нема в словнику
        fig.add_trace(go.Scatter(
            x=list(range(len(counts))),
            y=counts,
            mode='lines+markers',
            name=state.name,
            line=dict(color=color, width=2),
            marker=dict(size=6)
        ))

    fig.update_layout(
        title=dict(
            text="Динаміка станів",
            x=0.5, 
            xanchor='center'
        ),
        title_automargin=True,
        xaxis_title="Крок",
        yaxis_title="Кількість вузлів",
        xaxis=dict(range=[0, total_steps]),
        yaxis=dict(rangemode='tozero'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=350,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    container.plotly_chart(fig, use_container_width=True)


def plot_pie_chart(state_count, container, state2color, step=None):
    labels = [state.name for state in state_count.keys()]
    values = list(state_count.values())
    colors = [state2color[state] for state in state_count.keys()]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=colors),
        textinfo='percent',
        textfont=dict(color="black", size=20),
        insidetextorientation='auto'
    )])

    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        height=350,
        showlegend=False
    )

    container.plotly_chart(fig, use_container_width=False, key=f"pie_chart_step_{step}")