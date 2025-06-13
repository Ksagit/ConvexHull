import math


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
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2


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
                return sorted(
                    [p for p in unique_points if p == min_p or p == max_p],
                    key=lambda p: p.y,
                )
            return sorted([min_p, max_p], key=lambda p: (p.x, p.y))
        else:
            print("Otoczka wypukła jest trójkątem.")
            # Zwróć punkty posortowane wg. kąta, aby były w kolejności
            p0 = min(unique_points, key=lambda p: (p.y, p.x))
            sorted_points = sorted(
                unique_points,
                key=lambda p: (math.atan2(p.y - p0.y, p.x - p0.x), p.x, p.y),
            )
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

            cp = cross_product(
                current_point, dummy_prev_point if prev_point is None else prev_point, p
            )

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
        print(
            f"Otoczka wypukła jest wielokątem wypukłym o {num_vertices} wierzchołkach."
        )
    else:
        print("Brak punktów do wyznaczenia otoczki.")

    if num_vertices > 0:
        # Jarvis sam w sobie generuje ją w kolejności przeciwnie do ruchu wskazówek zegara.
        return hull
    else:
        return []
