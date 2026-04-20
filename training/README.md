# Pokazowy trening LoRA

Ten katalog jest oddzielony od aplikacji chatbota. Pliki tutaj nie są importowane przez `app.py` i nie wpływają na normalne uruchamianie projektu.

Zawartość:

- `chatbot_examples.jsonl` - mały pokazowy dataset rozmów.
- `requirements-train.txt` - zależności potrzebne do treningu.
- `train_lora.py` - przykładowy skrypt treningu adaptera LoRA.

## Ważne

To jest materiał pokazowy. Dataset ma zbyt mało przykładów, żeby realnie poprawić model. Do sensownego fine-tuningu potrzeba zwykle setek lub tysięcy spójnych przykładów.

Trening na CPU będzie bardzo wolny. Najlepiej uruchamiać go w Google Colab, Kaggle Notebook albo na komputerze z GPU NVIDIA.

## Instalacja zależności treningowych

Najlepiej użyć osobnego środowiska, żeby nie mieszać zależności aplikacji i treningu.

```powershell
python -m venv .venv-train
.\.venv-train\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r training\requirements-train.txt
```

## Uruchomienie

```powershell
python training\train_lora.py
```

Wynikowy adapter zostanie zapisany w:

```text
models/polka-lora-chatbot
```

## Co dalej

Aplikacja chatbota jeszcze nie ładuje adapterów LoRA. To celowo osobny etap. Żeby użyć wytrenowanego adaptera w aplikacji, trzeba dodać do `handlers/model_handler.py` obsługę `PeftModel.from_pretrained(...)` i zmienną środowiskową, np.:

```powershell
$env:CHATBOT_LORA_ADAPTER = "models/polka-lora-chatbot"
python app.py
```
