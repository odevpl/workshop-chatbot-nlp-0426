from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "chatbot.db"
TEMPLATES_PATH = BASE_DIR / "data" / "templates.json"
