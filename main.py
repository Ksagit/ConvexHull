import math
import matplotlib.pyplot as plt

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

def convex_hull_general(points):
    """
    Wyznacza otoczkę wypukłą dla dowolnej liczby punktów na płaszczyźnie
    przy użyciu algorytmu Monotone Chain.
    """
    if not points or len(points) == 0:
        return []

    # Usuń duplikaty. Używamy set do usuwania duplikatów.
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
            min_x = min(unique_points, key=lambda p: p.x)
            max_x = max(unique_points, key=lambda p: p.x)
            if min_x.x == max_x.x: # pionowa linia
                min_y = min(unique_points, key=lambda p: p.y)
                max_y = max(unique_points, key=lambda p: p.y)
                return sorted([min_y, max_y], key=lambda p: (p.y, p.x))
            else:
                return sorted([min_x, max_x], key=lambda p: (p.x, p.y))
        else:
            print("Otoczka wypukła jest trójkątem.")
            # Zwróć punkty posortowane wg. kąta, aby były w kolejności
            p0 = min(unique_points, key=lambda p: (p.y, p.x))
            sorted_points = sorted(unique_points, key=lambda p: (math.atan2(p.y - p0.y, p.x - p0.x), p.x, p.y))
            return sorted_points

    # Algorytm Monotone Chain dla n >= 4 punktów
    points_sorted = sorted(unique_points, key=lambda p: (p.x, p.y))

    upper_hull = []
    for p in points_sorted:
        while len(upper_hull) >= 2 and \
              cross_product(upper_hull[-2], upper_hull[-1], p) <= 0:
            upper_hull.pop()
        upper_hull.append(p)

    lower_hull = []
    for p in reversed(points_sorted):
        while len(lower_hull) >= 2 and \
              cross_product(lower_hull[-2], lower_hull[-1], p) <= 0:
            lower_hull.pop()
        lower_hull.append(p)

    hull = upper_hull[:-1] + lower_hull[:-1]
    final_hull = list(set(hull))

    # Analiza typu otoczki
    num_vertices = len(final_hull)

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
        p0 = min(final_hull, key=lambda p: (p.y, p.x))
        final_hull_sorted = sorted(final_hull,
                                   key=lambda p: (math.atan2(p.y - p0.y, p.x - p0.x),
                                                  dist_sq(p0, p)))
        return final_hull_sorted
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
    plt.title("Wizualizacja Otoczki Wypukłej")
    plt.grid(True)
    plt.axhline(0, color='gray', linewidth=0.5)
    plt.axvline(0, color='gray', linewidth=0.5)
    plt.legend()
    plt.axis('equal') # Zachowaj proporcje, aby okrąg wyglądał jak okrąg
    plt.show()


# --- Główna część programu ---

if __name__ == "__main__":
    print("--- Program do wyznaczania otoczki wypukłej ---")

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

    input_points = []
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

    print("\n--- Wynik ---")
    hull = convex_hull_general(input_points)

    if hull:
        print("Współrzędne kolejnych wierzchołków otoczki wypukłej:")
        for point in hull:
            print(f"  {point}")
    else:
        print("Nie można wyznaczyć otoczki wypukłej dla podanych punktów.")

    # --- Wizualizacja ---
    if input_points: # Wizualizuj tylko, jeśli są jakieś punkty wejściowe
        plot_hull(input_points, hull)

    print("\n--- Koniec programu ---")