import streamlit as st
from PIL import Image

st.set_page_config(page_title="Головна", layout="centered")
st.title("Моделювання поширення інформації в мережі")

st.markdown("""
**Цей застосунок дозволяє дослідити, як поширюється інформація в соціальній мережі за допомогою симуляцій на графах.**

У додатку доступні дві моделі симуляції, кожна з яких представлена на окремій сторінці:

:material/record_voice_over: **Однорідні джерела** — на цій сторінці можна змоделювати поширення дезінформації в мережі, де всі джерела мають однаковий вплив.

:material/bolt: **Інформаційне протистояння** — ця сторінка дозволяє змоделювати ситуацію, коли в мережі одночасно діють два типи джерел: ті, що поширюють дезінформацію, і ті, що намагаються її спростувати.
""")

st.markdown("""
На кожній сторінці ви можете або **створити мережу самостійно**, налаштувавши кількість вузлів, кластери (групи щільно пов'язаних між собою вузлів), ймовірності зв’язків тощо, або використати **автоматичне створення графа**. Автоматичне генерування пропонує два варіанти:
""")

col1, col2 = st.columns([1, 2])
with col1:
    st.image("app/assets/scale_free_graph.png", use_container_width=True)

with col2:
    st.markdown("""
    **Безмасштабна мережа** — мережа, де більшість вузлів мають мало зв’язків, а деякі — дуже багато.  
    Така топологія відповідає соціальним мережам, у яких окремі користувачі мають тисячі підписників,  
    а решта — взаємодіє з обмеженим колом осіб.  
    Наприклад, *Instagram* та *YouTube*.
    """)


col3, col4 = st.columns([1, 2])
with col3:
    st.image("app/assets/small_world_graph.png", use_container_width=True)
    # st.markdown("<p style='text-align: center; font-style: italic;'>Малосвітова мережа</p>", unsafe_allow_html=True)

with col4:
    st.markdown("""
    **Малосвітова мережа** — мережа, у якій більшість вузлів не є безпосередньо з’єднаними,  
    але будь-яку пару можна зв’язати через невелику кількість переходів.  
    Така структура є типовою для соціальних мереж, у яких користувачі утворюють щільні локальні спільноти,  
    але між ними існують короткі шляхи завдяки міжгруповим зв’язкам.  
    Прикладом можуть слугувати *Facebook* та *Viber*.
    """)

st.write("")
st.markdown("---")
st.write("")

st.markdown("#### Візуалізація процесу поширення інформації")

st.markdown("""
У кожній моделі ви можете спостерігати візуалізацію **поширення інформації безпосередньо на графі** (для мереж до 30 вузлів), 
а також **графік динаміки станів вузлів у часі** та **кругову діаграму поточного стану системи**. 
Ці візуалізації оновлюються на кожному кроці симуляції.
""")

st.markdown("#### :material/record_voice_over: Однорідні джерела")

col1, col2 = st.columns([3, 1.5])  
with col1:
    st.image("app/assets/simple_sim/graph.gif", use_container_width=True)

with col2:
    st.image("app/assets/simple_sim/pie_chart.gif", use_container_width=True)

st.image("app/assets/simple_sim/dynamics.png", use_container_width=True)


st.markdown("#### :material/bolt: Інформаційне протистояння")

col3, col4 = st.columns(2)
with col3:
    st.markdown("*Граф, що змінюється з часом:*")
    # TODO: вставити гіфку зміни графа
    # st.image("app/assets/gif_placeholder_antagonistic_graph.gif", use_container_width=True)

with col4:
    st.markdown("*Кругова діаграма станів вузлів:*")
    # TODO: вставити гіфку кругової діаграми
    # st.image("app/assets/gif_placeholder_antagonistic_pie.gif", use_container_width=True)

st.markdown("*Динаміка станів у часі:*")
# TODO: вставити гіфку графіку станів
# st.image("app/assets/gif_placeholder_antagonistic_line.gif", use_container_width=True)
