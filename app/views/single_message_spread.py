import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time

from simulation.generators.flexible_graph_builder import RemainingNodeStrategy, FlexibleGraphBuilder
from simulation.generators.graph_factory import GraphGeneratorFactory 
from simulation.models.single_message_model import SingleMessageSpreadModel
from utils.graph_visualization import visualize_graph, plot_state_dynamics, plot_pie_chart, safe_visualize
from utils.graph_utils import assign_random_sources_from_clusters
from simulation.models.state_enums import SINGLE_STATE2COLOR


st.set_page_config(layout="centered")
st.title("Модель поширення інформації від однорідних джерел")

if "graph_generation_method" not in st.session_state:
    st.session_state["graph_generation_method"] = None
if "graph" not in st.session_state:
    st.session_state["graph"] = None
if "are_clusters" not in st.session_state:
    st.session_state["are_clusters"] = None
if "cluster_config" not in st.session_state:
    st.session_state["cluster_config"] = None
if "source_distribution" not in st.session_state:
    st.session_state["source_distribution"] = None
if "outside_sources" not in st.session_state:
    st.session_state["outside_sources"] = None
if "cluster_map" not in st.session_state:
    st.session_state["cluster_map"] = None
if "sources_choosen" not in st.session_state:
    st.session_state["sources_choosen"] = False
if "simulation_set_up" not in st.session_state:
    st.session_state["simulation_set_up"] = False
if "simulation_mode" not in st.session_state:
    st.session_state["simulation_mode"] = None
if "simulation_steps" not in st.session_state:
    st.session_state["simulation_steps"] = None


# def safe_visualize(simulation, container, max_nodes=30, step=None):
#     num_nodes = simulation.get_num_nodes()
#     if num_nodes <= max_nodes:
#         simulation.visualize(container, step=step)
#         return True
#     else:
#         # container.info(
#         #     f"⚠️ Граф має {num_nodes} вузлів. "
#         #     f"Візуалізація відключена для графів із понад {max_nodes} вузлами, "
#         #     "оскільки вона значно сповільнює оновлення сторінки."
#         # )
#         return False


tab1, tab2 = st.tabs(["Власні налаштування", "Автоматичне генерування графа"])

with tab1:
    use_clusters = st.radio(
        label="**Створювати кластери при побудові графа?**",
        options=["Так", "Ні"],
        index=0,
        horizontal=True
    )

    with st.form("custom_graph_form"):
        total_nodes = st.number_input("Загальна кількість вузлів", min_value=1, value=4, step=1)

        cluster_sizes = []
        cluster_probs = []
        num_clusters = 0
        external_prob = 0.0
        remaining = 0
        add_remaining = "немає залишкових вузлів"

        if use_clusters == "Так":
            st.session_state["are_clusters"] = True

            num_clusters = st.number_input("Кількість кластерів", min_value=1, max_value=total_nodes, value=2, step=1)

            total_assigned = 0  

            for i in range(int(num_clusters)):
                st.markdown(
                    f"<div style='margin-bottom: 0.2rem; font-weight: 600;'>Налаштування кластера №{i+1}</div>",
                    unsafe_allow_html=True
                )

                cols = st.columns(2)
                with cols[0]:
                    max_available = total_nodes - total_assigned
                    default_value = min(2, max_available) if max_available > 0 else 0
                    size = st.number_input(
                        f"Кількість вузлів",
                        min_value=0,
                        max_value=total_nodes,
                        value=default_value,
                        key=f"size_{i}"
                    )
                with cols[1]:
                    prob = st.slider(
                        f"Ймовірність з'єднання",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.5,
                        key=f"prob_{i}"
                    )

                total_assigned += size
                cluster_sizes.append(size)
                cluster_probs.append(prob)

                if total_assigned > total_nodes:
                    st.toast(f"Загальна кількість вузлів у кластерах ({total_assigned}) перевищує допустиму ({total_nodes})", icon="⚠️")

            remaining = total_nodes - sum(cluster_sizes)

            intercluster_prob = st.slider(
                "Ймовірність з'єднання між кластерами",
                min_value=0.0,
                max_value=1.0,
                value=0.05
            )

            if remaining > 0:
                add_remaining = st.radio(
                    label="Що робити з залишковими вузлами?",
                    options=["Додати до кластерів випадково", "Залишити окремо"],
                    index=1,
                    key="add_remaining"
                )

                external_prob = st.slider(
                    "Ймовірність з'єднання залишкових вузлів з іншими",
                    0.0, 1.0, 0.2
                )

        else:
            st.session_state["are_clusters"] = False

            general_prob = st.slider("Ймовірність з'єднання між усіма вузлами", 0.0, 1.0, 0.1)
            

        submit_custom = st.form_submit_button("Згенерувати мережу")

        if submit_custom:
            builder = FlexibleGraphBuilder(total_nodes)

            if use_clusters == "Так":
                strategy = (
                    RemainingNodeStrategy.RANDOM
                    if add_remaining == "Додати до кластерів випадково"
                    else RemainingNodeStrategy.SEPARATE
                )

                st.session_state["cluster_config"] = {
                    "num_clusters": num_clusters,
                    "sizes": cluster_sizes,
                    "remaining": remaining,
                    "add_remaining": add_remaining
                }

                G = builder.build_clustered_graph(
                    cluster_sizes=cluster_sizes,
                    cluster_probs=cluster_probs,
                    intercluster_prob=intercluster_prob,
                    remaining_strategy=strategy,
                    external_prob=external_prob
                )

                st.session_state["cluster_map"] = builder.get_cluster_map()

            else:
                G = builder.build_flat_graph(general_prob)

            st.session_state.simulation = SingleMessageSpreadModel(G)

            st.success("Натиснули кнопку для створення налаштованого графа")
            st.session_state["graph_generation_method"] = "custom"


with tab2:
    generator_factory = GraphGeneratorFactory()

    graph_type = st.selectbox("Оберіть тип графа", generator_factory.list_generators())

    with st.form("auto_graph_form"):
        n = st.number_input("Кількість вузлів", min_value=2, value=10, key="auto_n")

        if graph_type == "Small-World Graph":
            k = st.slider("Кількість найближчих сусідів (k)", min_value=1, max_value=n - 1, value=min(4, n - 1), key="auto_k")
            p = st.slider("Ймовірність перез'єднання (p)", min_value=0.0, max_value=1.0, value=0.1, key="auto_p")
            params = (n, k, p)
        elif graph_type == "Scale-Free Graph":
            params = (n,)
        else:
            params = (n,)

        submitted = st.form_submit_button("Згенерувати мережу")

        if submitted:
            generator = generator_factory.get_generator(graph_type)
            if generator:
                G = generator(*params)
                st.session_state["graph"] = G
                st.session_state.simulation = SingleMessageSpreadModel(G)
                st.session_state["graph_generation_method"] = "auto"
                st.success("Граф успішно згенеровано.")
            else:
                st.error("Невідомий тип графа.")


if st.session_state.graph_generation_method is not None:
    st.session_state.simulation_steps_run = 0
    if st.session_state.simulation.graph is not None:
        col1, col2 = st.columns([1, 1])
        with col1:
            with st.popover("Обрати джерела"):
                st.number_input(
                    "Загальна кількість джерел",
                    min_value=1,
                    max_value=st.session_state.simulation.get_num_nodes(),
                    value=1,
                    key="total_sources"
                )

                if st.session_state.graph_generation_method == "custom" and st.session_state.are_clusters:
                    cluster_config = st.session_state.get("cluster_config", {})
                    num_clusters = cluster_config.get("num_clusters", 0)
                    cluster_sizes = cluster_config.get("sizes", [])
                    remaining = cluster_config.get("remaining", 0)
                    
                    total_sources_allocated = 0

                    for i, size in enumerate(cluster_sizes):
                        st.number_input(
                            f"Кількість джерел у кластері №{i+1}",
                            min_value=0,
                            max_value=size,
                            value=0,
                            key=f"source_cluster_{i}"
                        )
                        total_sources_allocated += st.session_state.get(f"source_cluster_{i}", 0)

                    if remaining > 0 and st.session_state.add_remaining == "Залишити окремо":
                        st.number_input(
                            "Кількість джерел серед залишкових вузлів",
                            min_value=0,
                            max_value=remaining,
                            value=0,
                            key="outside_sources"
                        )
                        if st.session_state.get("outside_sourses") is not None:
                            total_sources_allocated += st.session_state.get("outside_sources", 0)

                    if total_sources_allocated > st.session_state["total_sources"]:
                        st.error(f"⚠️ Загальна кількість джерел у кластерах ({total_sources_allocated}) перевищує допустиму ({st.session_state['total_sources']})")

                if st.button("Зберегти"):
                    st.session_state["sources_choosen"] = True

                    if st.session_state.graph_generation_method == "custom" and st.session_state.are_clusters:
                        num_clusters = st.session_state["cluster_config"]["num_clusters"]
                        
                        source_distribution = [
                            st.session_state.get(f"source_cluster_{i}", 0) for i in range(num_clusters)
                        ]
                        outside_sources = st.session_state.get("outside_sources", 0)
                        st.session_state["source_distribution"] = source_distribution
                    
                        selected_sources = assign_random_sources_from_clusters(st.session_state["cluster_map"], source_distribution, outside_sources)                       

                    else:
                        all_nodes = list(st.session_state.simulation.graph.nodes)
                        selected_sources = random.sample(all_nodes, st.session_state["total_sources"])

                    st.session_state.simulation.initialize(selected_sources)

        with col2:
            with st.popover("Симуляція"):
                if st.session_state["sources_choosen"]:
                    mode = st.radio(
                        "Оберіть режим симуляції:",
                        options=[
                            "Фіксована кількість ітерацій",
                            "До досягнення рівноваги (з обмеженням)"
                        ]
                    )

                    if mode == "Фіксована кількість ітерацій":
                        num_steps = st.number_input(
                            "Кількість ітерацій",
                            min_value=1,
                            max_value=1000,
                            value=10,
                            step=1
                        )
                        
                    elif mode == "До досягнення рівноваги (з обмеженням)":
                        max_steps = st.number_input(
                            "Максимальна кількість ітерацій",
                            min_value=1,
                            max_value=10000,
                            value=50,
                            step=1
                        )
                    
                    if st.button("Почати симуляцію"):
                        if mode == "Фіксована кількість ітерацій":
                            st.session_state["simulation_mode"] = "fixed"
                            st.session_state["simulation_steps"] = num_steps
                        else:
                            st.session_state["simulation_mode"] = "equilibrium"
                            st.session_state["simulation_max_steps"] = max_steps

                else:
                    st.warning("❗ Спершу збережіть налаштування для джерел.")

        
        visualization_placeholder = st.empty()
        line_chart_placeholder = st.empty()
        pie_chart_placeholder = st.empty()


        if st.session_state.simulation_mode == "fixed":
            for step in range(st.session_state.simulation_steps):
                st.session_state.simulation.step()
                st.session_state.simulation_steps_run += 1

                # st.session_state.simulation.visualize(visualization_placeholder, st.session_state.simulation_steps_run)
                safe_visualize(st.session_state.simulation, visualization_placeholder, step=st.session_state.simulation_steps_run)

                state_counts = st.session_state.simulation.state_counts  
                state_count_now = st.session_state.simulation.state_count  

                plot_state_dynamics(state_counts, line_chart_placeholder, total_steps=st.session_state.simulation_steps, state2color=SINGLE_STATE2COLOR)
                plot_pie_chart(state_count_now, pie_chart_placeholder, step=st.session_state.simulation_steps_run, state2color=SINGLE_STATE2COLOR)

                
                time.sleep(1)

        if (st.session_state.simulation_mode is None or st.session_state.simulation_steps_run == st.session_state.simulation_steps):
            if st.session_state.simulation_steps_run == st.session_state.simulation_steps:
                st.success("Симуляцію завершено — досягнуто максимальної кількості ітерацій.")

            # st.session_state.simulation.visualize(visualization_placeholder)
            safe_visualize(st.session_state.simulation, visualization_placeholder)

