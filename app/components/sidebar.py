import streamlit as st
from app.components.custom_styles import apply_custom_styles

def sidebar():
    apply_custom_styles()  # Викликаємо стилі
    st.sidebar.title("Меню")
    st.sidebar.write("Це бокове меню")
