import streamlit as st  # Biblioteka do tworzenia interfejsu webowego
import matplotlib.pyplot as plt
import pandas as pd
from main import (
    Point,
    convex_hull_jarvis,
)
import random  # Biblioteka do generowania liczb losowych


def setup_page():
    """Konfiguracja podstawowych ustawień strony."""
    st.set_page_config(page_title="Wizualizator Otoczki Wypukłej", layout="wide")
    st.title("Wizualizator Otoczki Wypukłej")
    st.write("Wizualizuj otoczkę wypukłą zbioru punktów za pomocą algorytmu Jarvisa.")


def display_csv_help():
    """Wyświetla informacje o wymaganej strukturze pliku CSV."""
    st.sidebar.markdown(
        """
    ### Wymagana struktura pliku CSV:
    - Plik musi zawierać dokładnie 2 kolumny
    - Pierwsza kolumna ZAWSZE oznacza współrzędną x, a druga y. Nazwy kolumn nie mają znaczenia
    - Wszystkie wartości muszą być liczbami
    - Plik musi zawierać co najmniej 2 punkty
    - Nie mogą występować puste wartości
    
    Uwaga: Dla 2 punktów otoczka wypukła będzie odcinkiem.
    
    Przykłady poprawnych plików CSV:
    
    Z nazwami kolumn:
    ```csv
    x,y
    0,0
    2,2
    ```
    
    Bez nazw kolumn:
    ```csv
    0,0
    2,2
    ```
    """
    )


def load_points_from_csv():
    """Wczytuje punkty z pliku CSV."""
    if "csv_points" not in st.session_state:
        st.session_state.csv_points = []

    # Wyświetl informacje o wymaganej strukturze
    display_csv_help()

    uploaded_file = st.sidebar.file_uploader("Wczytaj plik CSV", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            # Walidacja struktury pliku
            is_valid, errors = validate_csv_structure(df)

            if not is_valid:
                for error in errors:
                    st.error(error)
                return st.session_state.csv_points

            # Jeśli walidacja przeszła, konwertuj dane na punkty
            st.session_state.csv_points = [
                Point(row["x"], row["y"]) for _, row in df.iterrows()
            ]
            st.success("Plik CSV został poprawnie wczytany!")

        except Exception as e:
            st.error(f"Błąd odczytu pliku CSV: {str(e)}")
    return st.session_state.csv_points


def get_manual_points():
    """Pozwala użytkownikowi ręcznie wprowadzić punkty."""
    if "manual_points" not in st.session_state:
        st.session_state.manual_points = []

    st.sidebar.write("Wprowadź punkty ręcznie:")
    num_points = st.sidebar.number_input(
        "Liczba punktów", min_value=1, value=5, key="manual_num_points"
    )

    # Tworzenie nowych punktów tylko gdy zmieniła się liczba punktów
    if (
        "last_manual_num_points" not in st.session_state
        or st.session_state.last_manual_num_points != num_points
    ):
        st.session_state.manual_points = []
        st.session_state.last_manual_num_points = num_points

    # Uzupełnianie listy punktów jeśli jest za krótka
    while len(st.session_state.manual_points) < num_points:
        st.session_state.manual_points.append(Point(0.0, 0.0))

    # Aktualizacja współrzędnych punktów
    for i in range(num_points):
        col1, col2 = st.sidebar.columns(2)
        with col1:
            x = st.number_input(
                f"X{i+1}", value=st.session_state.manual_points[i].x, key=f"x{i}"
            )
        with col2:
            y = st.number_input(
                f"Y{i+1}", value=st.session_state.manual_points[i].y, key=f"y{i}"
            )
        st.session_state.manual_points[i] = Point(x, y)

    return st.session_state.manual_points[:num_points]


def generate_random_points():
    """Generuje losowe punkty na podstawie parametrów użytkownika."""
    if "random_points" not in st.session_state:
        st.session_state.random_points = []

    st.sidebar.write("Wygeneruj punkty losowe:")
    num_points = st.sidebar.number_input(
        "Liczba punktów losowych",
        min_value=3,
        max_value=100,
        value=10,
        key="random_num_points",
    )
    x_range = st.sidebar.slider("Zakres X", 0, 1000, (0, 100), key="x_range")
    y_range = st.sidebar.slider("Zakres Y", 0, 1000, (0, 100), key="y_range")

    if (
        st.sidebar.button("Wygeneruj punkty losowe", key="generate_random")
        or "last_random_num_points" not in st.session_state
        or st.session_state.last_random_num_points != num_points
        or st.session_state.last_x_range != x_range
        or st.session_state.last_y_range != y_range
    ):
        st.session_state.random_points = [
            Point(
                random.uniform(x_range[0], x_range[1]),
                random.uniform(y_range[0], y_range[1]),
            )
            for _ in range(num_points)
        ]
        st.session_state.last_random_num_points = num_points
        st.session_state.last_x_range = x_range
        st.session_state.last_y_range = y_range

    return st.session_state.random_points


def get_points_from_input():
    """Pobiera punkty na podstawie wybranej metody wprowadzania."""
    input_method = st.sidebar.radio(
        "Wybierz sposób wprowadzania punktów:",
        ["Wczytaj CSV", "Wprowadź ręcznie", "Punkty losowe"],
        key="input_method",
    )

    if input_method == "Wczytaj CSV":
        return load_points_from_csv()
    elif input_method == "Wprowadź ręcznie":
        return get_manual_points()
    elif input_method == "Punkty losowe":
        return generate_random_points()
    return []


def create_plot(points, hull):
    """Tworzy wykres z punktami i otoczką wypukłą."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Rysowanie wszystkich punktów wejściowych
    all_x = [p.x for p in points]
    all_y = [p.y for p in points]
    ax.plot(all_x, all_y, "o", color="blue", label="Punkty wejściowe")

    # Rysowanie otoczki wypukłej
    if len(hull) > 0:
        hull_x = [p.x for p in hull]
        hull_y = [p.y for p in hull]

        if len(hull) > 1:
            hull_x.append(hull[0].x)
            hull_y.append(hull[0].y)
            ax.plot(hull_x, hull_y, "-r", linewidth=2, label="Otoczka wypukła")
            ax.plot(
                hull_x[:-1],
                hull_y[:-1],
                "s",
                color="red",
                markersize=8,
                label="Wierzchołki otoczki",
            )
        else:
            ax.plot(
                hull_x,
                hull_y,
                "s",
                color="red",
                markersize=8,
                label="Wierzchołek otoczki",
            )

    # Konfiguracja wykresu
    ax.set_xlabel("Współrzędna X")
    ax.set_ylabel("Współrzędna Y")
    ax.set_title("Wizualizacja Otoczki Wypukłej")
    ax.grid(True)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.axvline(0, color="gray", linewidth=0.5)
    ax.legend()
    ax.axis("equal")

    return fig


def display_hull_info(hull):
    """Wyświetla informacje o otoczce wypukłej i umożliwia eksport do CSV."""
    st.subheader("Informacje o otoczce wypukłej")
    if len(hull) > 0:
        st.write(f"Liczba wierzchołków otoczki: {len(hull)}")
        st.write(
            "Wierzchołki otoczki (w kolejności przeciwnie do ruchu wskazówek zegara):"
        )

        # Tworzenie DataFrame z punktami otoczki
        hull_data = pd.DataFrame({"x": [p.x for p in hull], "y": [p.y for p in hull]})

        # Wyświetlanie tabeli z punktami
        st.dataframe(hull_data)

        # Przycisk do eksportu do CSV
        if st.button("Eksportuj otoczkę do CSV"):
            # Konwersja DataFrame do CSV
            csv = hull_data.to_csv(index=False)

            # Tworzenie pliku do pobrania
            st.download_button(
                label="Pobierz plik CSV",
                data=csv,
                file_name="convex_hull_points.csv",
                mime="text/csv",
            )
    else:
        st.write("Nie można obliczyć otoczki wypukłej.")


def validate_csv_structure(df):
    """Waliduje strukturę pliku CSV."""
    errors = []

    # Sprawdzenie liczby kolumn
    if len(df.columns) != 2:
        errors.append("Plik CSV musi zawierać dokładnie 2 kolumny")
        return False, errors

    # Sprawdzenie nazw kolumn (jeśli są zdefiniowane)
    if df.columns[0] != "x" or df.columns[1] != "y":
        # Jeśli nazwy kolumn są niepoprawne, zmień je na domyślne
        df.columns = ["x", "y"]

    # Sprawdzenie typów danych
    try:
        df["x"] = pd.to_numeric(df["x"])
        df["y"] = pd.to_numeric(df["y"])
    except ValueError:
        errors.append("Wszystkie wartości muszą być liczbami")
        return False, errors

    # Sprawdzenie czy są jakieś wartości NaN
    if df.isnull().any().any():
        errors.append("Plik nie może zawierać pustych wartości")
        return False, errors

    # Sprawdzenie minimalnej liczby punktów
    if len(df) < 2:
        errors.append("Plik musi zawierać co najmniej 2 punkty")
        return False, errors

    return True, []


def main():
    """Główna funkcja aplikacji."""
    setup_page()
    st.sidebar.header("Opcje wprowadzania")

    points = get_points_from_input()

    if points:
        hull = convex_hull_jarvis(points)
        fig = create_plot(points, hull)
        st.pyplot(fig)
        display_hull_info(hull)
    else:
        st.info("Dodaj punkty za pomocą opcji w pasku bocznym.")


if __name__ == "__main__":
    main()
