# Co trzeba zrobić, żeby rozpocząć uczenie modelu

Żeby realnie rozpocząć uczenie modelu, trzeba przygotować osobną ścieżkę treningową. Obecna aplikacja umie używać modelu, ale trening powinien być oddzielony od kodu chatbota.

## 1. Wybrać metodę

Nie warto trenować całego modelu od zera ani robić pełnego fine-tuningu wszystkich wag. Dla modelu `eryk-mazus/polka-1.1b-chat` sensowna metoda to LoRA albo QLoRA.

LoRA oznacza, że:

- model bazowy zostaje bez zmian,
- uczymy mały adapter,
- po treningu aplikacja może ładować model bazowy razem z adapterem.

To jest dużo lżejsze niż pełny fine-tuning.

## 2. Przygotować dane

Trzeba utworzyć plik z przykładami rozmów, np.:

```text
training/chatbot_examples.jsonl
```

Format jednej linii:

```jsonl
{"messages":[{"role":"user","content":"Cześć"},{"role":"assistant","content":"Cześć! Jak mogę pomóc?"}]}
```

Przykład:

```jsonl
{"messages":[{"role":"user","content":"Podaj przepis na ciasto do pizzy"},{"role":"assistant","content":"Wymieszaj mąkę, wodę, drożdże, sól i oliwę. Wyrabiaj kilka minut i odstaw do wyrośnięcia."}]}
```

Orientacyjnie:

- minimum pokazowe: 50-100 przykładów,
- sensowny start: 500+ przykładów,
- lepiej: 1000-3000 spójnych przykładów.

Jeśli danych będzie mało, model może nauczyć się stylu odpowiedzi, ale niekoniecznie nowej wiedzy.

## 3. Dodać zależności treningowe

Najlepiej użyć osobnego pliku:

```text
training/requirements-train.txt
```

Przykładowe zależności:

```txt
datasets
accelerate
peft
trl
transformers
torch
```

Dla QLoRA często dochodzi:

```txt
bitsandbytes
```

Na Windowsie `bitsandbytes` bywa problematyczne, więc do startu lepiej przygotować zwykłe LoRA albo uruchamiać trening w Colab/Kaggle/Linux.

## 4. Dodać skrypt treningowy

Przykładowy plik:

```text
training/train_lora.py
```

Skrypt powinien:

1. Wczytać model bazowy `eryk-mazus/polka-1.1b-chat`.
2. Wczytać tokenizer.
3. Wczytać dataset JSONL.
4. Zamienić `messages` na tekst przez `chat_template`.
5. Skonfigurować LoRA.
6. Uruchomić trening.
7. Zapisać adapter do katalogu, np.:

```text
models/polka-lora-chatbot
```

## 5. Przygotować sprzęt

Na CPU trening będzie bardzo wolny i raczej niepraktyczny. Może trwać wiele godzin lub dni nawet dla małego datasetu.

Lepsze opcje:

- Google Colab z GPU,
- Kaggle Notebook z GPU,
- lokalna karta NVIDIA,
- Linux albo WSL2, jeśli używamy GPU.

Dla modelu około 1.1B parametrów zwykłe LoRA może wymagać sensownej ilości VRAM. QLoRA jest lżejsze, ale bardziej problematyczne środowiskowo.

## 6. Po treningu podłączyć adapter do aplikacji

Obecna aplikacja ładuje model mniej więcej tak:

```python
pipeline("text-generation", model=MODEL_NAME)
```

Po treningu LoRA trzeba byłoby ładować model bazowy i adapter:

```python
base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model = PeftModel.from_pretrained(base_model, "models/polka-lora-chatbot")
```

Można dodać zmienną środowiskową:

```powershell
$env:CHATBOT_LORA_ADAPTER = "models/polka-lora-chatbot"
python app.py
```

To powinien być osobny etap po przygotowaniu i przetestowaniu treningu.

## 7. Testować jakość

Po treningu trzeba porównać:

- model bazowy,
- model z adapterem.

Przykładowe pytania testowe:

```text
Jak zrobić pizzę?
Podaj szybki przepis na zupę.
Co potrafisz?
Dlaczego odpowiadasz wolno?
Jak zmienić nazwę rozmowy?
```

Warto testować pytania, których nie było dokładnie w danych treningowych.

## Minimalny checklist

Żeby rozpocząć, trzeba przygotować:

```text
training/
├── chatbot_examples.jsonl
├── requirements-train.txt
├── train_lora.py
└── README.md
```

Następnie:

1. Zebrać 50-100 przykładów rozmów na pokaz.
2. Odpalić trening w Colab/Kaggle/GPU.
3. Zapisać adapter LoRA.
4. Dodać do aplikacji opcjonalne ładowanie adaptera.

## Najbardziej praktyczne podejście

Najpierw warto przygotować infrastrukturę treningową i przykładowy dataset. Sam trening można potraktować jako osobny etap, bo wymaga GPU i większej liczby dobrych danych.
