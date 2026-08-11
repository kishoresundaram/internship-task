import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

if not GEMINI_MODEL:
    raise ValueError("GEMINI_MODEL not found in .env")

print("Gemini API key loaded successfully")
print(f"Gemini model: {GEMINI_MODEL}")