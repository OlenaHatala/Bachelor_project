import streamlit as st
import networkx as nx
import time

from simulation.generators.flexible_graph_builder import RemainingNodeStrategy, FlexibleGraphBuilder
from simulation.models.antagonistic_spread_model import AntagonisticSpreadModel
from utils.graph_utils import assign_sources_dual
from simulation.models.state_enums import ANTAGONISTIC_STATE2COLOR
from utils.graph_visualization import plot_pie_chart, plot_state_dynamics

st.set_page_config(layout="centered")
st.title("Модель впливу протилежних джерел у мережі")

st.session_state.current_page = "antag_scrs"
if "antag_scrs__are_clusters" not in st.session_state:
    st.session_state["antag_scrs__are_clusters"] = None
if "antag_scrs__cluster_config" not in st.session_state:
    st.session_state["antag_scrs__cluster_config"] = None
if "antag_srcs__cluster_map" not in st.session_state:
    st.session_state["antag_srcs__cluster_map"] = None
if "antag_srcs__graph_generation_method" not in st.session_state:
    st.session_state["antag_srcs__graph_generation_method"] = None
if "antag_simulation_mode" not in st.session_state:
    st.session_state["antag_simulation_mode"] = None
if "antag_simulation_steps" not in st.session_state:
    st.session_state["antag_simulation_steps"] = None
if "antag_simulation_max_steps" not in st.session_state:
    st.session_state["antag_simulation_max_steps"] = None

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
            st.session_state["antag_scrs__are_clusters"] = True

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
            st.session_state["antag_scrs__are_clusters"] = False

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

                st.session_state["antag_scrs__cluster_config"] = {
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

                # print("\nПриналежність вузлів до кластерів")
                # cluster_map = builder.get_cluster_map()
                # st.session_state["cluster_map"] = cluster_map

                st.session_state["antag_srcs__cluster_map"] = builder.get_cluster_map()

                # for cluster_id in sorted(cluster_map.keys(), key=lambda x: (999 if x == "around" else x)):
                #     if cluster_id == "around":
                #         print("**Залишкові вузли (поза кластерами):**", sorted(cluster_map[cluster_id]))
                #     else:
                #         print(f"**Кластер {cluster_id}:**", sorted(cluster_map[cluster_id]))

            else:
                G = builder.build_flat_graph(general_prob)

            st.session_state.antag_simulation = AntagonisticSpreadModel(G)

            st.success("Натиснули кнопку для створення налаштованого графа")
            st.session_state["antag_srcs__graph_generation_method"] = "custom"


with tab2:
    with st.form("auto_graph_form"):
        graph_type = st.selectbox("Оберіть тип графа", [
            "Fast GNP Random Graph",
            "GNP Random Graph",
            "Barabasi-Albert Graph",
            "Scale-Free Graph"
        ])
        # n = st.number_input("Кількість вузлів", min_value=1, value=10)

        # if graph_type in ["Fast GNP Random Graph", "GNP Random Graph"]:
        #     p = st.slider("Ймовірність з'єднання", min_value=0.0, max_value=1.0, value=0.1)
        #     params = (n, p)
        # elif graph_type == "Barabasi-Albert Graph":
        #     m = st.slider("Кількість підключень нового вузла", min_value=1, max_value=max(1, n - 1), value=1)
        #     params = (n, m)
        # elif graph_type == "Scale-Free Graph":
        #     params = (n,)
        # else:
        #     params = (n,)

        # submitted = st.form_submit_button("Згенерувати мережу")

        # if submitted:
        #     if graph_type == "Fast GNP Random Graph":
        #         G = nx.fast_gnp_random_graph(*params, seed=42)
        #     elif graph_type == "GNP Random Graph":
        #         G = nx.gnp_random_graph(*params, seed=42)
        #     elif graph_type == "Barabasi-Albert Graph":
        #         G = nx.barabasi_albert_graph(*params, seed=42)
        #     elif graph_type == "Scale-Free Graph":
        #         G = nx.scale_free_graph(*params, seed=42).to_undirected()
        #     else:
        #         G = nx.empty_graph(n)


        #     st.session_state["graph"] = G

        #     st.success("Натиснули кнопку для створення автоматичного графа")
        #     st.session_state["graph_generation_method"] = "auto"


if st.session_state.antag_srcs__graph_generation_method is not None:
    st.session_state.antag__simulation_steps_run = 0

    st.markdown("### Налаштування джерел поширення")

    colA, colB = st.columns(2)

    with colA:
        with st.expander("🔴 Джерела типу A", expanded=False):
            total_sources_A = st.number_input(
                "Загальна кількість джерел A",
                min_value=0,
                max_value=st.session_state.antag_simulation.get_num_nodes(),
                value=0,
                key="total_sources_A"
            )

            total_sources_A_allocated = 0

            if st.session_state["antag_scrs__are_clusters"]:
                cluster_config = st.session_state.get("antag_scrs__cluster_config", {})
                cluster_sizes = cluster_config.get("sizes", [])
                remaining = cluster_config.get("remaining", 0)

                for i, size in enumerate(cluster_sizes):
                    st.number_input(
                        f"Кількість джерел A у кластері №{i+1}",
                        min_value=0,
                        max_value=size,
                        value=0,
                        key=f"source_A_cluster_{i}"
                    )
                    total_sources_A_allocated += st.session_state.get(f"source_A_cluster_{i}", 0)

                if remaining > 0 and st.session_state.get("add_remaining") == "Залишити окремо":
                    st.number_input(
                        "Джерела A серед залишкових вузлів",
                        min_value=0,
                        max_value=remaining,
                        value=0,
                        key="outside_sources_A"
                    )
                    total_sources_A_allocated += st.session_state.get("outside_sources_A", 0)

                if total_sources_A_allocated > total_sources_A:
                    st.error(f"⚠️ Джерел A у кластерах більше ({total_sources_A_allocated}), ніж задано ({total_sources_A})")

            if st.button("Зберегти джерела A"):
                st.session_state["sources_A_saved"] = True
                # st.success("Налаштування джерел A збережено")

    with colB:
        with st.expander("🔵 Джерела типу B", expanded=False):
            total_sources_B = st.number_input(
                "Загальна кількість джерел B",
                min_value=0,
                max_value=st.session_state.antag_simulation.get_num_nodes(),
                value=0,
                key="total_sources_B"
            )

            total_sources_B_allocated = 0

            if st.session_state["antag_scrs__are_clusters"]:
                cluster_config = st.session_state.get("antag_scrs__cluster_config", {})
                cluster_sizes = cluster_config.get("sizes", [])
                remaining = cluster_config.get("remaining", 0)

                for i, size in enumerate(cluster_sizes):
                    st.number_input(
                        f"Кількість джерел B у кластері №{i+1}",
                        min_value=0,
                        max_value=size,
                        value=0,
                        key=f"source_B_cluster_{i}"
                    )
                    total_sources_B_allocated += st.session_state.get(f"source_B_cluster_{i}", 0)

                if remaining > 0 and st.session_state.get("add_remaining") == "Залишити окремо":
                    st.number_input(
                        "Джерела B серед залишкових вузлів",
                        min_value=0,
                        max_value=remaining,
                        value=0,
                        key="outside_sources_B"
                    )
                    total_sources_B_allocated += st.session_state.get("outside_sources_B", 0)

                if total_sources_B_allocated > total_sources_B:
                    st.error(f"⚠️ Джерел B у кластерах більше ({total_sources_B_allocated}), ніж задано ({total_sources_B})")

            if st.button("Зберегти джерела B"):
                st.session_state["sources_B_saved"] = True
                # st.success("Налаштування джерел B збережено")


    # Якщо обидва типи джерел збережено, викликаємо функцію призначення та ініціалізацію моделі
    if st.session_state.get("sources_A_saved") and st.session_state.get("sources_B_saved"):
        cluster_map = st.session_state.get("antag_srcs__cluster_map", {})
        cluster_config = st.session_state.get("antag_scrs__cluster_config", {})
        total_nodes = st.session_state.antag_simulation.get_num_nodes()

        num_clusters = cluster_config.get("num_clusters", 0)
        cluster_sizes = cluster_config.get("sizes", [])
        remaining = cluster_config.get("remaining", 0)

        dist_A = [st.session_state.get(f"source_A_cluster_{i}", 0) for i in range(num_clusters)]
        outside_A = st.session_state.get("outside_sources_A", 0)
        # print(f"\ndist_A = {dist_A}")
        # print(f"outside_A = {outside_A}")

        dist_B = [st.session_state.get(f"source_B_cluster_{i}", 0) for i in range(num_clusters)]
        outside_B = st.session_state.get("outside_sources_B", 0)
        # print(f"dist_B = {dist_B}")
        # print(f"outside_B = {outside_B}")

        try:
            sources_A, sources_B = assign_sources_dual(
                cluster_map=cluster_map,
                source_dist_A=dist_A,
                outside_A=outside_A,
                source_dist_B=dist_B,
                outside_B=outside_B,
                total_nodes=total_nodes
            )

            # print(f"sources_A = {sources_A}")
            # print(f"sources_B = {sources_B}")

            # ініціалізуємо модель
            st.session_state.antag_simulation.initialize(sources_A, sources_B)
            st.session_state["antag_sources_chosen"] = True
            st.success("Обидва типи джерел збережено та застосовано.")
        except ValueError as e:
            st.error(f"Помилка під час розподілу джерел: {str(e)}")



        with st.popover("Симуляція"):
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
                    st.session_state["antag_simulation_mode"] = "fixed"
                    st.session_state["antag_simulation_steps"] = num_steps
                else:
                    st.session_state["antag_simulation_mode"] = "equilibrium"
                    st.session_state["antag_simulation_max_steps"] = max_steps

                st.session_state["antag_simulation_started"] = True
    else:
        with st.popover("Симуляція"):
            st.warning("❗ Спочатку потрібно зберегти налаштування для обох типів джерел A та B.")



    graph_placeholder = st.empty()
    plot_placeholder = st.empty()
    pie_placeholder = st.empty()

    if st.session_state.antag_simulation_mode == "fixed":
        for step in range(st.session_state.antag_simulation_steps):
            st.session_state.antag_simulation.step()
            st.session_state.antag__simulation_steps_run += 1

            st.session_state.antag_simulation.visualize(graph_placeholder, st.session_state.antag__simulation_steps_run)

            state_counts = st.session_state.antag_simulation.state_counts
            state_count_now = st.session_state.antag_simulation.state_count

            plot_state_dynamics(state_counts, plot_placeholder, st.session_state.antag_simulation_steps, ANTAGONISTIC_STATE2COLOR)
            plot_pie_chart(state_count_now, pie_placeholder, ANTAGONISTIC_STATE2COLOR, step=st.session_state.antag__simulation_steps_run)

            time.sleep(1)



    if (st.session_state.antag_simulation_mode is None or st.session_state.antag__simulation_steps_run == st.session_state.antag_simulation_steps):
        if st.session_state.antag__simulation_steps_run == st.session_state.antag_simulation_steps:
            st.success("Симуляцію завершено — досягнуто максимальної кількості ітерацій.")

    st.session_state.antag_simulation.visualize(graph_placeholder)