
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

MODEL_NAME = "gemini-3.5-flash-lite"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

CHECKPOINT_DIR = os.path.join(BASE_DIR, "checkpoints")
