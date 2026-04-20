from config import (
    MODEL_CONTEXT_MESSAGES,
    MODEL_DO_SAMPLE,
    MODEL_ENABLED,
    MODEL_MAX_NEW_TOKENS,
    MODEL_NAME,
    TORCH_NUM_THREADS,
)


_generator = None
_load_error = None


def _load_generator():
    global _generator, _load_error
    if _generator is not None:
        return _generator
    if _load_error is not None:
        raise RuntimeError(_load_error)

    try:
        import torch
        from transformers import pipeline

        if TORCH_NUM_THREADS > 0:
            torch.set_num_threads(TORCH_NUM_THREADS)

        _generator = pipeline("text-generation", model=MODEL_NAME, device=-1)
        return _generator
    except Exception as exc:
        _load_error = str(exc)
        raise RuntimeError(_load_error) from exc


def build_messages(history, user_message):
    recent = history[-MODEL_CONTEXT_MESSAGES:]
    messages = [
        {
            "role": "system",
            "content": (
                "Jesteś pomocnym chatbotem. Odpowiadaj po polsku, krótko i konkretnie. "
                "Odpowiadaj maksymalnie jednym lub dwoma zdaniami. Jeśli użytkownik prosi o długą treść, "
                "podaj zwięzły początek i zaproponuj kontynuację."
            ),
        }
    ]
    for message in recent:
        role = "user" if message["role"] == "user" else "assistant"
        messages.append({"role": role, "content": message["content"]})
    messages.append({"role": "user", "content": user_message})
    return messages


def build_fallback_prompt(messages):
    lines = [messages[0]["content"], ""]
    for message in messages[1:]:
        role = "Użytkownik" if message["role"] == "user" else "Asystent"
        lines.append(f"{role}: {message['content']}")
    lines.append("Asystent:")
    return "\n".join(lines)


def build_prompt(generator, history, user_message):
    messages = build_messages(history, user_message)
    tokenizer = generator.tokenizer
    if getattr(tokenizer, "chat_template", None):
        return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return build_fallback_prompt(messages)


def clean_response(text):
    response = text.strip()
    for marker in [
        "<|user|>",
        "<|assistant|>",
        "<|system|>",
        "<|im_start|>",
        "<|im_end|>",
        "Użytkownik:",
        "Asystent:",
        "User:",
        "Assistant:",
    ]:
        if marker in response:
            response = response.split(marker, 1)[0].strip()
    response = response.strip(" -\t\r\n")
    sentence_endings = [index for index, char in enumerate(response) if char in ".!?" and index >= 8]
    if len(sentence_endings) >= 2:
        return response[: sentence_endings[1] + 1].strip()
    return response


def generate_response(messages, user_message):
    if not MODEL_ENABLED:
        return "Model jest wyłączony zmienną CHATBOT_DISABLE_MODEL=1."

    try:
        generator = _load_generator()
        prompt = build_prompt(generator, messages, user_message)
        generation_options = {
            "max_new_tokens": MODEL_MAX_NEW_TOKENS,
            "do_sample": MODEL_DO_SAMPLE,
            "repetition_penalty": 1.1,
            "no_repeat_ngram_size": 3,
            "pad_token_id": generator.tokenizer.eos_token_id,
            "num_return_sequences": 1,
            "return_full_text": False,
        }
        if MODEL_DO_SAMPLE:
            generation_options.update({"temperature": 0.7, "top_p": 0.9})

        output = generator(prompt, **generation_options)[0]["generated_text"]
        response = clean_response(output)
        return response or "Nie wiem jeszcze, jak odpowiedzieć na to pytanie."
    except Exception:
        return "Model nie jest teraz dostępny. Sprawdź instalację zależności albo nazwę modelu w CHATBOT_MODEL."
