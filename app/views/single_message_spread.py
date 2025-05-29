import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

from simulation.generators.flexible_graph_builder import RemainingNodeStrategy, FlexibleGraphBuilder

st.set_page_config(layout="centered")
st.title("Модель поширення інформації від однорідних джерел")

tab1, tab2 = st.tabs(["Власні налаштування", "Автоматичне генерування графа"])

with tab1:

    use_clusters = st.radio(
        label="**Створювати кластери при побудові графа?**",
        options=["Так", "Ні"],
        index=1,
        horizontal=True
    )

    with st.form("custom_graph_form"):
        total_nodes = st.number_input("Загальна кількість вузлів", min_value=1, value=2, step=1)
        

        cluster_sizes = []
        cluster_probs = []
        # remaining = total_nodes
        num_clusters = 0
        external_prob = 0.0
        remaining = 0
        add_remaining = "немає залишкових вузлів"

        if use_clusters == "Так":
            num_clusters = st.number_input("Кількість кластерів", min_value=1, max_value=total_nodes, value=2, step=1)

            # st.markdown("**Налаштування кластерів**")

            total_assigned = 0  

            for i in range(int(num_clusters)):
                # st.markdown(f"**Налаштування кластера №{i+1}**")
                st.markdown(
                    f"<div style='margin-bottom: 0.2rem; font-weight: 600;'>Налаштування кластера №{i+1}</div>",
                    unsafe_allow_html=True
                )
                # st.markdown(f"<div class='cluster-title'>Налаштування кластера №{i+1}</div>", unsafe_allow_html=True)

                cols = st.columns(2)
                with cols[0]:
                    max_available = total_nodes - total_assigned
                    default_value = min(1, max_available) if max_available > 0 else 0
                    size = st.number_input(
                        # f"Кількість вузлів у кластері №{i+1}",
                        f"Кількість вузлів",
                        min_value=0,
                        max_value=total_nodes,
                        value=default_value,
                        key=f"size_{i}"
                    )
                with cols[1]:
                    prob = st.slider(
                        # f"Ймовірність з'єднання у кластері №{i+1}",
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
                    index=0
                )

                external_prob = st.slider(
                    "Ймовірність з'єднання залишкових вузлів з іншими",
                    0.0, 1.0, 0.2
                )


        else:
            general_prob = st.slider("Ймовірність з'єднання між усіма вузлами", 0.0, 1.0, 0.1)

        submit_custom = st.form_submit_button("Згенерувати мережу")

        if submit_custom:
            pass



with tab2:
    with st.form("auto_graph_form"):
        graph_type = st.selectbox("Оберіть тип графа", [
            "Fast GNP Random Graph",
            "GNP Random Graph",
            "Barabasi-Albert Graph",
            "Scale-Free Graph"
        ])
        n = st.number_input("Кількість вузлів", min_value=1, value=10)

        if graph_type in ["Fast GNP Random Graph", "GNP Random Graph"]:
            p = st.slider("Ймовірність з'єднання", min_value=0.0, max_value=1.0, value=0.1)
            params = (n, p)
        elif graph_type == "Barabasi-Albert Graph":
            m = st.slider("Кількість підключень нового вузла", min_value=1, max_value=max(1, n - 1), value=1)
            params = (n, m)
        elif graph_type == "Scale-Free Graph":
            params = (n,)
        else:
            params = (n,)

        submitted = st.form_submit_button("Згенерувати мережу")

        if submitted:
            if graph_type == "Fast GNP Random Graph":
                G = nx.fast_gnp_random_graph(*params, seed=42)
            elif graph_type == "GNP Random Graph":
                G = nx.gnp_random_graph(*params, seed=42)
            elif graph_type == "Barabasi-Albert Graph":
                G = nx.barabasi_albert_graph(*params, seed=42)
            elif graph_type == "Scale-Free Graph":
                G = nx.scale_free_graph(*params, seed=42).to_undirected()
            else:
                G = nx.empty_graph(n)

            st.success(f"Граф згенеровано: {G.number_of_nodes()} вузлів, {G.number_of_edges()} ребер")
            pos = nx.spring_layout(G, seed=42)
            fig, ax = plt.subplots()
            nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
            st.pyplot(fig)
