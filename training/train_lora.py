from pathlib import Path

from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer


BASE_MODEL = "eryk-mazus/polka-1.1b-chat"
DATASET_PATH = Path(__file__).with_name("chatbot_examples.jsonl")
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "models" / "polka-lora-chatbot"


def format_example(example, tokenizer):
    messages = example["messages"]
    if getattr(tokenizer, "chat_template", None):
        return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)

    lines = []
    for message in messages:
        role = "Użytkownik" if message["role"] == "user" else "Asystent"
        lines.append(f"{role}: {message['content']}")
    return "\n".join(lines)


def main():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)
    dataset = load_dataset("json", data_files=str(DATASET_PATH), split="train")

    dataset = dataset.map(
        lambda example: {"text": format_example(example, tokenizer)},
        remove_columns=dataset.column_names,
    )

    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )

    training_args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        num_train_epochs=1,
        learning_rate=2e-4,
        logging_steps=5,
        save_strategy="epoch",
        fp16=False,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=512,
        peft_config=lora_config,
        args=training_args,
    )
    trainer.train()
    trainer.save_model(str(OUTPUT_DIR))
    tokenizer.save_pretrained(str(OUTPUT_DIR))
    print(f"Adapter LoRA zapisany w: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
