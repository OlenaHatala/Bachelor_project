import streamlit as st

def apply_custom_styles():
    st.markdown(
        """
        <style>
        /* Зміна кольору бокового меню */
        [data-testid="stSidebar"] {
            background-color: #2E4053 !important; /* Темно-синій фон */
        }

        /* Зміна шрифту заголовків у боковому меню */
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #FFFFFF !important; /* Білий колір */
            font-size: 20px !important;
        }

        /* Зміна розміру тексту у боковому меню */
        [data-testid="stSidebar"] p {
            font-size: 16px !important;
            color: #D5D8DC !important; /* Світло-сірий */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
