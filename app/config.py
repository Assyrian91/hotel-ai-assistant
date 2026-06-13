from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
DB_PATH = os.getenv("DB_PATH", "./data/hotel.db")
DOCS_PATH = os.getenv("DOCS_PATH", "./data/docs")
FAISS_PATH = "./data/faiss_index"
