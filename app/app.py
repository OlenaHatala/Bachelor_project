import streamlit as st

temp = st.Page("views/Trying.py", title="TEMP")
home_page = st.Page("views/home.py", title="Головна", icon=":material/home:")
basic_simulation_page = st.Page("views/basic_simulation.py", title="First Simulation", icon=":material/play_circle:")
complex_simulation_page = st.Page("views/complex_simulation.py", title="Complex Simulation", icon=":material/analytics:")

simulation_pages = [basic_simulation_page, complex_simulation_page]

single_info_simulation = st.Page("views/single_message_spread.py", title="Однорідні джерела")

pg = st.navigation({
    "": [home_page],
    "Симуляції": [single_info_simulation],
    # "Simulations": simulation_pages, 
    "----------issues----------": [basic_simulation_page, temp]
    })

pg.run()