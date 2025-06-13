# Convex Hull

Aplikacja do wizualizacji otoczki wypukłej zbioru punktów za pomocą algorytmu Jarvisa.

## Wymagania

- Python 3.x
- pip (menedżer pakietów Pythona)

## Instalacja i uruchomienie

1. Sklonuj repozytorium:
```bash
git clone <url-repozytorium>
cd ConvexHull
```

2. Utwórz i aktywuj wirtualne środowisko:

Na systemach Unix/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Na systemie Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Zainstaluj wymagane zależności:
```bash
pip install -r requirements.txt
```

4. Uruchom aplikację:
```bash
streamlit run app.py
```

Aplikacja zostanie uruchomiona w domyślnej przeglądarce pod adresem http://localhost:8501

## Funkcjonalności

- Wczytywanie punktów z pliku CSV
- Ręczne wprowadzanie punktów
- Generowanie losowych punktów
- Wizualizacja otoczki wypukłej
- Eksport wyników do pliku CSV

## Dezaktywacja środowiska wirtualnego

Po zakończeniu pracy z projektem, możesz dezaktywować środowisko wirtualne komendą:
```bash
deactivate
```
