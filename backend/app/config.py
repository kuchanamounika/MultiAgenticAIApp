import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "multi-agentic-ai")
ENV = os.getenv("ENV", "dev")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://user:pass@localhost:5432/aiapp")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
