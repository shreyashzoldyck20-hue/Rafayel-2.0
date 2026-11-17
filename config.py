import os
from dotenv import load_dotenv

load_dotenv()

CLOUD_BASE_URL = os.getenv("CLOUD_BASE_URL", "").rstrip("/")
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY", "")
CLOUD_MODEL = os.getenv("CLOUD_MODEL", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
DATABASE_PATH = os.getenv("DATABASE_PATH", "rafayel.db")
