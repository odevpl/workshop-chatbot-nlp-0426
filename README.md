# Python Chatbot - warsztat

Lokalny chatbot webowy napisany w Pythonie i Flasku. Projekt pokazuje, jak połączyć klasyczną aplikację webową z prostą logiką regułową i lokalnym modelem językowym.

Chatbot potrafi:

- prowadzić rozmowę w przeglądarce,
- zapisywać rozmowy w lokalnej bazie SQLite,
- liczyć proste działania matematyczne,
- odpowiadać na znane pytania z pliku JSON,
- używać lokalnego modelu chatowego jako fallbacku,
- działać bez logowania i bez kont użytkowników.

Domyślny model:

```text
eryk-mazus/polka-1.1b-chat
```

Model jest uruchamiany lokalnie przez HuggingFace Transformers.

## Dla Kogo

Ten projekt jest przygotowany pod warsztat. Część osób może znać Pythona, ale instrukcja zakłada, że można startować od zera.

Nie musisz wcześniej znać:

- Flask,
- SQLite,
- HuggingFace,
- modeli językowych,
- JavaScript `fetch`.

Podstawowa znajomość terminala pomaga, ale nie jest wymagana.

## Co Trzeba Zainstalować

Przed warsztatem zainstaluj:

1. Python 3.12 albo nowszy z serii 3.x  
   Pobieranie: https://www.python.org/downloads/

2. Git  
   Pobieranie: https://git-scm.com/downloads

3. Visual Studio Code  
   Pobieranie: https://code.visualstudio.com/

4. Przeglądarka, np. Chrome, Edge albo Firefox.

Podczas instalacji Pythona na Windowsie zaznacz opcję:

```text
Add Python to PATH
```

## Sprawdzenie Instalacji

Otwórz PowerShell i sprawdź:

```powershell
python --version
pip --version
git --version
```

Przykładowy poprawny wynik:

```text
Python 3.12.4
pip 26.0.1
git version 2.x.x
```

Jeśli `python` nie działa, zamknij i otwórz PowerShell ponownie. Jeśli dalej nie działa, Python prawdopodobnie nie został dodany do `PATH`.

## Pobranie Projektu

Jeśli korzystasz z Git:

```powershell
git clone ADRES_REPOZYTORIUM
cd PhytonChatbot
```

Jeśli masz projekt jako ZIP:

1. Rozpakuj ZIP.
2. Otwórz folder projektu w VS Code.
3. Otwórz terminal w VS Code: `Terminal -> New Terminal`.

W dalszych przykładach zakładamy, że jesteś w katalogu projektu:

```text
c:\Projects\PhytonChatbot
```

## Utworzenie Środowiska

W katalogu projektu uruchom:

```powershell
python -m venv .venv
```

To tworzy lokalne środowisko Pythona tylko dla tego projektu.

Aktywacja środowiska:

```powershell
.\.venv\Scripts\Activate.ps1
```

Po aktywacji powinno być widać prefix:

```text
(.venv) PS C:\Projects\PhytonChatbot>
```

Jeśli PowerShell zablokuje aktywację skryptów, uruchom:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Ta zmiana działa tylko w aktualnym oknie terminala.

## Instalacja Zależności

Po aktywacji `.venv` uruchom:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Instalacja może potrwać kilka minut, ponieważ `torch` i `transformers` są większymi paczkami.

W projekcie używane są m.in.:

- `Flask` - backend webowy,
- `Flask-Cors` - obsługa CORS,
- `transformers` - ładowanie modelu,
- `torch` - uruchamianie modelu,
- `numpy` - zależność używana przez PyTorch.

## Uruchomienie Projektu

W aktywnym środowisku `.venv` uruchom:

```powershell
python app.py
```

W terminalu powinno pojawić się:

```text
Running on http://127.0.0.1:5000
```

Otwórz w przeglądarce:

```text
http://127.0.0.1:5000
```

Zatrzymanie serwera:

```powershell
Ctrl+C
```

## Pierwszy Test

Po uruchomieniu aplikacji wpisz w czacie:

```text
hej
```

To powinno zwrócić szybką odpowiedź z pliku `data/templates.json`.

Potem wpisz:

```text
ile to jest 2 + 2?
```

To powinno zwrócić:

```text
Wynik: 4
```

Następnie wpisz pytanie, którego nie ma w szablonach, np.:

```text
Podaj prosty pomysł na obiad
```

To pytanie trafi do lokalnego modelu. Pierwsza odpowiedź może potrwać dłużej.

## Ważne: Pobieranie Modelu

Pierwsze pytanie wysłane do modelu może uruchomić pobieranie plików z HuggingFace.

W terminalu możesz zobaczyć pliki takie jak:

```text
config.json
model.safetensors
tokenizer_config.json
generation_config.json
```

To normalne. Główny plik modelu może mieć ponad 1 GB.

Po pobraniu model zostaje w lokalnym cache, więc kolejne uruchomienia zwykle nie pobierają go od nowa.

## Dlaczego Model Odpowiada Wolno

Model działa lokalnie na CPU. To oznacza, że odpowiedź może trwać od kilku do kilkudziesięciu sekund.

Szybkie są:

- matematyka,
- szablony JSON,
- operacje na bazie SQLite.

Wolniejsze są:

- pytania ogólne, które idą do modelu.

Domyślnie odpowiedzi modelu są krótkie:

```text
CHATBOT_MAX_NEW_TOKENS = 60
```

Większa wartość daje dłuższe odpowiedzi, ale spowalnia generowanie.

## Konfiguracja Modelu

Zmiana długości odpowiedzi:

```powershell
$env:CHATBOT_MAX_NEW_TOKENS = "100"
python app.py
```

Zmiana modelu:

```powershell
$env:CHATBOT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
python app.py
```

Uruchomienie bez modelu, tylko z matematyką i szablonami:

```powershell
$env:CHATBOT_DISABLE_MODEL = "1"
python app.py
```

Sterowanie liczbą wątków CPU dla PyTorch:

```powershell
$env:CHATBOT_TORCH_THREADS = "4"
python app.py
```

Włączenie bardziej losowych odpowiedzi:

```powershell
$env:CHATBOT_DO_SAMPLE = "1"
python app.py
```

Zmienne środowiskowe ustawione w ten sposób działają w aktualnym oknie PowerShell.

## Struktura Projektu

Najważniejsze pliki i foldery:

```text
app.py                    start aplikacji Flask
config.py                 konfiguracja ścieżek i modelu
requirements.txt          zależności aplikacji
README.md                 instrukcja projektu

data/
  templates.json          szablony odpowiedzi

database/
  db_init.py              tworzenie tabel SQLite
  database.py             funkcje do obsługi bazy

handlers/
  chat_logic.py           kolejność logiki: math -> template -> model
  math_handler.py         kalkulator matematyczny
  template_handler.py     dopasowanie szablonów JSON
  model_handler.py        obsługa lokalnego modelu

routes/
  conversations.py        endpointy rozmów
  messages.py             endpointy wiadomości

static/
  index.html              interfejs aplikacji
  css/style.css           style
  js/api.js               komunikacja z API
  js/chat.js              renderowanie czatu
  js/sidebar.js           lista rozmów
  js/title.js             edycja tytułu rozmowy

steps/                    etapy warsztatowe
training/                 pokazowe pliki do fine-tuningu
```

## Etapy Warsztatowe

Folder `steps/` zawiera gotowe snapshoty kolejnych etapów pracy:

```text
steps/
├── 01_szkielet_projektu
├── 02_frontend_chat
├── 03_templates_json
├── 04_math_handler
├── 05_sqlite_historia
├── 06_wiele_rozmow_api
├── 07_model_lokalny
├── 08_training_pokazowy
└── 09_wersja_finalna
```

Każdy etap ma folder `gotowe/`, czyli kopię plików dla danego momentu warsztatu.

## Szablony Odpowiedzi

Szablony znajdują się w:

```text
data/templates.json
```

Przykład:

```json
{
  "tag": "greeting",
  "patterns": ["hello", "hej"],
  "responses": ["Cześć! Jak mogę pomóc?"]
}
```

Zmiana `templates.json` nie wymaga restartu serwera. Plik jest wczytywany przy każdym dopasowaniu.

## Baza Danych

Aplikacja używa SQLite. Plik bazy powstaje automatycznie:

```text
database/chatbot.db
```

Baza nie jest dodawana do Gita, bo to lokalny plik roboczy.

Jeśli chcesz zacząć od pustej historii, zatrzymaj serwer i usuń:

```text
database/chatbot.db
```

Po kolejnym uruchomieniu aplikacja utworzy bazę od nowa.

## API

Endpointy rozmów:

```text
GET    /api/conversations
POST   /api/conversations
PATCH  /api/conversations/<id>
DELETE /api/conversations/<id>
```

Endpointy wiadomości:

```text
GET  /api/conversations/<id>/messages
POST /api/conversations/<id>/messages
```

## Pokazowy Trening Modelu

Folder `training/` jest pokazowy i nie wpływa na działanie aplikacji.

Zawiera:

```text
training/chatbot_examples.jsonl
training/requirements-train.txt
training/train_lora.py
training/jak_uczyc.md
```

To materiał do omówienia fine-tuningu LoRA. Trening najlepiej uruchamiać na GPU, np. w Colab albo Kaggle, a nie lokalnie na CPU.

## Typowe Problemy

### PowerShell blokuje aktywację `.venv`

Uruchom:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### `ModuleNotFoundError: No module named 'flask'`

Najczęściej zależności zostały zainstalowane poza `.venv`.

Sprawdź, czy widzisz:

```text
(.venv)
```

Potem uruchom:

```powershell
pip install -r requirements.txt
```

### Model długo nie odpowiada

To normalne przy pierwszym uruchomieniu albo na słabszym CPU.

Możesz zmniejszyć limit odpowiedzi:

```powershell
$env:CHATBOT_MAX_NEW_TOKENS = "40"
python app.py
```

### Chcę szybko testować bez modelu

Uruchom:

```powershell
$env:CHATBOT_DISABLE_MODEL = "1"
python app.py
```

Wtedy działają szablony, matematyka, baza i UI, ale pytania ogólne nie idą do modelu.

### Po zmianach w JavaScript przeglądarka pokazuje starą wersję

Odśwież stronę twardo:

```text
Ctrl+F5
```

## Przydatne Komendy

Aktywacja środowiska:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalacja zależności:

```powershell
pip install -r requirements.txt
```

Start aplikacji:

```powershell
python app.py
```

Zatrzymanie aplikacji:

```text
Ctrl+C
```

Sprawdzenie statusu Gita:

```powershell
git status
```

## Czego Uczymy Się W Projekcie

- podstaw Flask,
- komunikacji frontend-backend przez JSON,
- pracy z SQLite,
- obsługi plików JSON,
- prostego routingu logiki chatbota,
- bezpiecznego liczenia wyrażeń matematycznych,
- użycia lokalnego modelu językowego,
- ograniczeń modeli działających lokalnie na CPU,
- przygotowania danych do przyszłego fine-tuningu.
