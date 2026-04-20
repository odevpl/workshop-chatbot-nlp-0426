# Python Chatbot - warsztat - założenia

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
git clone https://github.com/odevpl/workshop-chatbot-nlp-0426.git
cd workshop-chatbot-nlp-0426
```

Jeśli masz projekt jako ZIP:

1. Rozpakuj ZIP.
2. Otwórz folder projektu w VS Code.
3. Otwórz terminal w VS Code: `Terminal -> New Terminal`.

W dalszych przykładach zakładamy, że jesteś w katalogu projektu:

```text
c:\Projects\workshop-chatbot-nlp-0426
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
(.venv) PS C:\Projects\workshop-chatbot-nlp-0426>
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

Po uruchomieniu aplikacji otwórz w przeglądarce:

```text
http://127.0.0.1:5000
```

Powinna pojawić się strona startowa z informacją, że Flask działa.

Następnie sprawdź endpoint kontrolny:

```text
http://127.0.0.1:5000/api/health
```

Powinien zwrócić odpowiedź JSON:

```json
{
  "status": "ok"
}
```
