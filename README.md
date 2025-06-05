# Bachelor_project

Цей проєкт є дипломною роботою на тему **"Симуляція поширення дезінформації у соціальних мережах"**. У рамках проєкту реалізовано симулятор з графовими моделями розповсюдження інформації з використанням бібліотек Python та інтерфейсу Streamlit.

## 📌 Функціональність

- Два типи моделей:
  - **Однорідне поширення** (SingleMessageSpreadModel) — базується на зміні опору вузлів.
  - **Антагоністичні джерела** (AntagonisticSpreadModel) — враховується довіра до джерел.
- Підтримка кількох типів графів:
  - Scale-Free
  - Small-World
  - Власні графи з кластерами або без.
- Візуалізація графа на кожному кроці симуляції (за умови, що кількість вершин не перевищує 30).
- Побудова графіків динаміки станів.

## 🗂 Структура проєкту
```
Bachelor_project/
│
├── app/                           # Основна логіка застосунку
│   ├── simulation/
│   │   ├── generators/            # Генерація графів
│   │   │   ├── flexible_graph_builder.py
│   │   │   └── graph_factory.py
│   │   └── models/                # Моделі поширення
│   │       ├── antagonistic_spread_model.py
│   │       ├── single_message_model.py
│   │       └── state_enums.py
│   ├── utils/                     # Утиліти для графів та візуалізації
│   │   ├── graph_utils.py
│   │   └── graph_visualization.py
│   └── views/                     # Сторінки Streamlit
│       ├── home.py
│       ├── single_message_spread.py
│       └── antagonistic_sources.py
│
├── app.py                         # Точка входу для запуску Streamlit
├── requirements.txt               # Список залежностей
├── README.md                      # Цей файл
└── .gitignore

````

## Перед початком роботи переконайтеся, що у вас встановлено:
- Python 3.9 або вище


## 🛠 Встановлення

1. **Клонувати репозиторій:**

```bash
git clone https://github.com/OlenaHatala/Bachelor_project.git
cd Bachelor_project
````

2. **Створити віртуальне середовище (рекомендується):**

```bash
python -m venv venv
source venv/bin/activate       # для Linux/Mac
venv\Scripts\activate.bat      # для Windows
```

3. **Встановити залежності:**

```bash
pip install -r requirements.txt
```

## 🚀 Запуск застосунку

```bash
streamlit run app/app.py
```

---
## 📎 Ліцензія

Цей проєкт призначений для освітніх цілей. Будь-яке використання частин коду в комерційних проєктах — лише з дозволу автора.
