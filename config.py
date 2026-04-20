from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "chatbot.db"
TEMPLATES_PATH = BASE_DIR / "data" / "templates.json"

MODEL_NAME = os.getenv("CHATBOT_MODEL", "eryk-mazus/polka-1.1b-chat")
MODEL_MAX_NEW_TOKENS = int(os.getenv("CHATBOT_MAX_NEW_TOKENS", "60"))
MODEL_CONTEXT_MESSAGES = 6
MODEL_ENABLED = os.getenv("CHATBOT_DISABLE_MODEL", "").lower() not in {
    "1",
    "true",
    "yes",
    "on",
}
MODEL_DO_SAMPLE = os.getenv("CHATBOT_DO_SAMPLE", "").lower() in {"1", "true", "yes", "on"}
TORCH_NUM_THREADS = int(os.getenv("CHATBOT_TORCH_THREADS", "0"))
