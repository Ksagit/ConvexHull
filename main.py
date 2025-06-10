import math
import matplotlib.pyplot as plt
import csv # Import modułu csv

class Point:
    """Reprezentuje punkt na płaszczyźnie."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

def cross_product(o, a, b):
    """
    Oblicza iloczyn wektorowy dla wektorów OA i OB.
    Służy do określania orientacji trzech punktów (o, a, b):
    - > 0: a-b-o tworzy lewoskrętny skręt (przeciwnie do ruchu wskazówek zegara)
    - < 0: a-b-o tworzy prawoskrętny skręt (zgodnie z ruchem wskazówek zegara)
    - = 0: punkty są współliniowe
    """
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

def dist_sq(p1, p2):
    """Oblicza kwadrat odległości między dwoma punktami."""
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2

def convex_hull_jarvis(points):
    """
    Wyznacza otoczkę wypukłą dla dowolnej liczby punktów na płaszczyźnie
    przy użyciu algorytmu Jarvisa (Wrapped Gift).
    """
    if not points or len(points) == 0:
        return []

    # Usuń duplikaty
    unique_points = list(set(points))
    n = len(unique_points)

    if n <= 1:
        print("Otoczka wypukła jest punktem.")
        return unique_points
    elif n == 2:
        print("Otoczka wypukła jest odcinkiem.")
        return sorted(unique_points, key=lambda p: (p.x, p.y))
    elif n == 3:
        # Sprawdź, czy punkty są współliniowe
        if cross_product(unique_points[0], unique_points[1], unique_points[2]) == 0:
            print("Otoczka wypukła jest odcinkiem (trzy punkty współliniowe).")
            # Znajdź punkty skrajne
            min_p = min(unique_points, key=lambda p: (p.x, p.y))
            max_p = max(unique_points, key=lambda p: (p.x, p.y))
            # Obsługa pionowej linii: sortuj po Y
            if min_p.x == max_p.x:
                return sorted([p for p in unique_points if p == min_p or p == max_p], key=lambda p: p.y)
            return sorted([min_p, max_p], key=lambda p: (p.x, p.y))
        else:
            print("Otoczka wypukła jest trójkątem.")
            # Zwróć punkty posortowane wg. kąta, aby były w kolejności
            p0 = min(unique_points, key=lambda p: (p.y, p.x))
            sorted_points = sorted(unique_points, key=lambda p: (math.atan2(p.y - p0.y, p.x - p0.x), p.x, p.y))
            return sorted_points

    # Algorytm Jarvisa dla n >= 4 punktów
    # 1. Znajdź punkt o najmniejszej współrzędnej Y (a w przypadku remisu, najmniejszej X)
    # To będzie nasz punkt początkowy otoczki.
    start_point = min(unique_points, key=lambda p: (p.y, p.x))

    hull = []
    current_point = start_point
    prev_point = None

    # "Sztuczny" punkt, aby poprawnie obliczyć pierwszy kąt
    # Wybieramy punkt na lewo od start_point, żeby pierwszy skręt był na prawo
    # To pozwala nam znaleźć pierwszy najbardziej lewoskrętny punkt.
    dummy_prev_point = Point(current_point.x - 1, current_point.y)

    while True:
        hull.append(current_point)
        
        # Znajdź następny punkt, który tworzy najbardziej lewoskrętny skręt
        # z current_point i (previous_point dla current_point)
        next_point = None

        for p in unique_points:
            if p == current_point:
                continue

            cp = cross_product(current_point, dummy_prev_point if prev_point is None else prev_point, p)

            # Bardziej solidna logika dla Jarvisa:
            # Ustaw kandydata na następny punkt jako pierwszy dostępny punkt (p).
            if next_point is None:
                next_point = p
            else:
                val = cross_product(current_point, next_point, p)
                if val > 0:  # 'p' jest bardziej "lewoskrętne" niż 'next_point'
                    next_point = p
                elif val == 0:  # 'p' jest współliniowe z 'current_point' i 'next_point'
                    # Jeśli są współliniowe, wybierz ten, który jest dalej
                    if dist_sq(current_point, p) > dist_sq(current_point, next_point):
                        next_point = p

        prev_point = current_point
        current_point = next_point

        if current_point == start_point:
            break

    # Analiza typu otoczki
    num_vertices = len(hull)

    if num_vertices == 1:
        print("Otoczka wypukła jest punktem.")
    elif num_vertices == 2:
        print("Otoczka wypukła jest odcinkiem.")
    elif num_vertices == 3:
        print("Otoczka wypukła jest trójkątem.")
    elif num_vertices == 4:
        print("Otoczka wypukła jest czworokątem.")
    elif num_vertices > 4:
        print(f"Otoczka wypukła jest wielokątem wypukłym o {num_vertices} wierzchołkach.")
    else:
        print("Brak punktów do wyznaczenia otoczki.")

    if num_vertices > 0:
        # Jarvis sam w sobie generuje ją w kolejności przeciwnie do ruchu wskazówek zegara.
        return hull
    else:
        return []

def plot_hull(all_points, hull_points):
    """
    Wizualizuje punkty wejściowe i wyznaczoną otoczkę wypukłą.
    """
    plt.figure(figsize=(8, 8))

    # Narysuj wszystkie punkty wejściowe
    all_x = [p.x for p in all_points]
    all_y = [p.y for p in all_points]
    plt.plot(all_x, all_y, 'o', color='blue', label='Punkty wejściowe')

    # Narysuj wierzchołki otoczki wypukłej i połącz je liniami
    if len(hull_points) > 0:
        hull_x = [p.x for p in hull_points]
        hull_y = [p.y for p in hull_points]

        # Zamknij pętlę, dodając pierwszy punkt na końcu, aby linia była zamknięta
        if len(hull_points) > 1:
            hull_x.append(hull_points[0].x)
            hull_y.append(hull_points[0].y)
            plt.plot(hull_x, hull_y, '-r', linewidth=2, label='Otoczka wypukła')
            plt.plot(hull_x, hull_y, 's', color='red', markersize=8, label='Wierzchołki otoczki')
        else: # Jeśli otoczka to tylko punkt
            plt.plot(hull_x, hull_y, 's', color='red', markersize=8, label='Wierzchołek otoczki')

    plt.xlabel("Współrzędna X")
    plt.ylabel("Współrzędna Y")
    plt.title("Wizualizacja Otoczki Wypukłej (Algorytm Jarvisa)")
    plt.grid(True)
    plt.axhline(0, color='gray', linewidth=0.5)
    plt.axvline(0, color='gray', linewidth=0.5)
    plt.legend()
    plt.axis('equal') # Zachowaj proporcje, aby okrąg wyglądał jak okrąg
    plt.show()

def load_points_from_csv(filename):
    """
    Wczytuje punkty z pliku CSV. Oczekiwany format: x,y
    """
    points = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if len(row) == 2:
                    try:
                        x = float(row[0].strip())
                        y = float(row[1].strip())
                        points.append(Point(x, y))
                    except ValueError:
                        print(f"Ostrzeżenie: Pomięto nieprawidłowy wiersz {i+1} w pliku CSV: '{', '.join(row)}'. Oczekiwano dwóch liczb.")
                else:
                    print(f"Ostrzeżenie: Pomięto nieprawidłowy format wiersza {i+1} w pliku CSV: '{', '.join(row)}'. Oczekiwano 'x,y'.")
        return points
    except FileNotFoundError:
        print(f"Błąd: Plik '{filename}' nie został znaleziony.")
        return []
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd podczas wczytywania pliku CSV: {e}")
        return []

# --- Główna część programu ---

if __name__ == "__main__":
    print("--- Program do wyznaczania otoczki wypukłej (Algorytm Jarvisa) ---")

    input_points = []
    
    while True:
        print("\nWybierz sposób wprowadzania punktów:")
        print("1. Wprowadź punkty ręcznie z klawiatury")
        print("2. Wczytaj punkty z pliku CSV")
        choice = input("Wybór (1/2): ").strip()

        if choice == '1':
            while True:
                try:
                    num_points_str = input("Podaj liczbę punktów (min. 1): ")
                    num_points = int(num_points_str)
                    if num_points < 1:
                        print("Liczba punktów musi być większa lub równa 1. Spróbuj ponownie.")
                        continue
                    break
                except ValueError:
                    print("Nieprawidłowa liczba. Proszę wprowadzić liczbę całkowitą.")

            for i in range(num_points):
                while True:
                    try:
                        x_str = input(f"Podaj współrzędną X dla punktu {i+1}: ")
                        y_str = input(f"Podaj współrzędną Y dla punktu {i+1}: ")
                        x = float(x_str)
                        y = float(y_str)
                        input_points.append(Point(x, y))
                        break
                    except ValueError:
                        print("Nieprawidłowa współrzędna. Proszę wprowadzić liczbę (np. 3 lub 3.5).")
            break # Wyjście z pętli wyboru po wprowadzeniu ręcznym
        elif choice == '2':
            input_points = load_points_from_csv("points.csv")
            if not input_points: # Jeśli plik pusty lub błąd, daj szansę na ponowne wprowadzenie
                print("Nie wczytano żadnych punktów z pliku CSV. Spróbuj ponownie lub wybierz inny sposób.")
                continue
            break # Wyjście z pętli wyboru po wczytaniu z CSV
        else:
            print("Nieprawidłowy wybór. Proszę wybrać 1 lub 2.")

    print("\n--- Wynik ---")
    hull = convex_hull_jarvis(input_points)

    if hull:
        print("Współrzędne kolejnych wierzchołków otoczki wypukłej (zgodnie z ruchem przeciwnym do wskazówek zegara):")
        for point in hull:
            print(f"  {point}")
    else:
        print("Nie można wyznaczyć otoczki wypukłej dla podanych punktów.")

    # --- Wizualizacja ---
    if input_points: # Wizualizuj tylko, jeśli są jakieś punkty wejściowe
        plot_hull(input_points, hull)
    else:
        print("Brak punktów do wizualizacji.")


    print("\n--- Koniec programu ---")