import streamlit as st

home_page = st.Page("pages/home.py", title="Home", icon=":material/home:")
basic_simulation_page = st.Page("pages/basic_simulation.py", title="First Simulation", icon=":material/help:")
complex_simulation_page = st.Page("pages/complex_simulation.py", title="Complex Simulation", icon=":material/settings:")

simulation_pages = [basic_simulation_page, complex_simulation_page]


pg = st.navigation({
    "": [home_page],
    "Simulation": simulation_pages
    })

pg.run()