# Arkatar World Studio

Narzędzie do budowy i utrzymywania bazy wiedzy o świecie fantasy, zarządzania relacjami między bytami, prowadzenia osi czasu wydarzeń i symulacji historii.

## Funkcjonalności

- **Zarządzanie bytami**: Lokacje, frakcje, postacie, religie, przedmioty
- **System relacji**: Sojusze, wrogość, zależności między bytami
- **Oś czasu**: Chronologia wydarzeń w świecie
- **Symulacja historii**: Automatyczne generowanie konfliktów i wydarzeń
- **Story Arcs**: Projektowanie kampanii i questów
- **Eksport**: Generowanie dokumentacji w formacie Markdown/JSON
- **CLI**: Interfejs wiersza poleceń dla zaawansowanych operacji

## Stos technologiczny

### Backend
- Python 3.x
- FastAPI (REST API)
- SQLite + SQLAlchemy (ORM)
- pytest (testy)

### Frontend
- React + TypeScript
- Vite (build tool)
- Vitest + Testing Library (testy)

### CLI
- Python (argparse)

## Instalacja i uruchomienie

### Wymagania
- Python 3.9+
- Node.js 18+
- npm lub yarn

### Backend

1. Przejdź do katalogu backend:
```bash
cd backend
```

2. Utwórz wirtualne środowisko:
```bash
python -m venv venv
```

3. Aktywuj środowisko:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

5. Uruchom serwer:
```bash
uvicorn app.main:app --reload
```

Backend będzie dostępny pod adresem: http://localhost:8000

### Frontend

1. Przejdź do katalogu frontend:
```bash
cd frontend
```

2. Zainstaluj zależności:
```bash
npm install
```

3. Uruchom serwer deweloperski:
```bash
npm run dev
```

Frontend będzie dostępny pod adresem: http://localhost:5173

### CLI

Z poziomu głównego katalogu projektu:

```bash
python arkatar_cli.py --help
```

Przykłady użycia:
```bash
# Lista postaci
python arkatar_cli.py list-characters

# Lista frakcji
python arkatar_cli.py list-factions

# Eksport do Markdown
python arkatar_cli.py export-markdown --output ./export

# Symulacja
python arkatar_cli.py simulate --ticks 10
```

## Testy

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## Struktura projektu

```
fantasy-world/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database configuration
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── crud/                # CRUD operations
│   │   ├── routes/              # API endpoints
│   │   ├── simulation.py        # History simulation engine
│   │   └── export_markdown.py  # Markdown export logic
│   ├── tests/                   # Backend tests
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── api/                 # API client
│   │   ├── components/          # React components
│   │   ├── views/               # Page views
│   │   ├── tests/               # Frontend tests
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── arkatar_cli.py               # CLI tool
├── README.md
└── TEST_PLAN.md                 # Test plan documentation

```

## API Documentation

Po uruchomieniu backendu, dokumentacja API dostępna jest pod adresami:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Rozwój projektu

Projekt został zbudowany zgodnie z metodologią TDD (Test-Driven Development). Każda funkcjonalność jest pokryta testami jednostkowymi i integracyjnymi.

### Możliwe rozszerzenia
- Zaawansowana wizualizacja grafu relacji (D3.js, Cytoscape)
- Integracja z generatorami tekstu (AI)
- Eksport do formatów specyficznych dla silników RPG
- System wersjonowania historii świata
- Współpraca wieloużytkownikowa
- Import danych z innych formatów (JSON, XML)

## Licencja

MIT

## Autorzy

Projekt "Arkatar World Studio"
