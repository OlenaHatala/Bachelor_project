import streamlit as st

home_page = st.Page("views/home.py", title="Головна", icon=":material/home:")

single_info_simulation = st.Page("views/single_message_spread.py", title="Однорідні джерела", icon=":material/record_voice_over:")
antagonistic_scrs = st.Page("views/antagonistic_sources.py", title="Інформаційне протистояння", icon=":material/bolt:")

pg = st.navigation({
    "": [home_page],
    "Симуляції": [single_info_simulation, antagonistic_scrs],
    })

pg.run()