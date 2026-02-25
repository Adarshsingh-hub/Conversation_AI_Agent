import os 

from dotenv import load_dotenv
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL","gpt-4o-mini")
    EMBED_MODEL = os.getenv("EMBED_MODEL","text-embedding-3-small")
    CHROMA_PATH = os.getenv("CHROMA_PATH","./chroma_db")
    DATA_PATH = os.getenv("DATA_PATH","./data")
    # Retrieval
    TOP_K = int(os.getenv("TOP_K","5"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS","1000"))
    
SYSTEM_PROMPT = (
    "You are a helpful customer support agent for Digimind. "
    "Answer questions ONLY using the context provided. "
    "If the answer is not in the context, say: "
    "'I don't have that info -- contact support@digimind.in' "
    "Be concise, friendly and professional."
)

config = Config()