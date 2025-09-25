import os
from dotenv import load_dotenv

load_dotenv()

# Sikkerhedstjek for API-nøgle
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required. Please add it to your .env file.")

# Sikkerhedstjek for placeholder-værdier
if OPENAI_API_KEY == "DIN-OPENAI-API-NOEGLE-HER" or OPENAI_API_KEY == "sk-proj-DIN-OPENAI-API-NOEGLE-HER":
    raise ValueError(
        "🔒 SIKKERHEDSFEJL: Du skal erstatte placeholder-værdien i .env filen med din rigtige OpenAI API-nøgle!\n"
        "1. Gå til https://platform.openai.com/api-keys\n"
        "2. Generer en ny API-nøgle\n"
        "3. Erstat 'DIN-OPENAI-API-NOEGLE-HER' i .env filen\n"
        "4. ALDRIG del denne nøgle offentligt!"
    )

# Advarsel for gamle/eksponerede nøgler (eksempel patterns)
suspicious_patterns = [
    "sk-proj-HppE2OPz",  # Eksempel på potentielt eksponeret nøgle
    "test-key",
    "example-key"
]

for pattern in suspicious_patterns:
    if OPENAI_API_KEY.startswith(pattern):
        print(f"⚠️  ADVARSEL: Din API-nøgle ser ud til at være et eksempel eller potentielt kompromitteret.")
        print(f"   Overvej at regenerere en ny nøgle på https://platform.openai.com/api-keys")
        break

EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
CHAT_MODEL  = os.getenv("CHAT_MODEL", "gpt-4o-mini")
TOP_K = int(os.getenv("TOP_K", "6"))
CHUNK_SIZE_CHARS = int(os.getenv("CHUNK_SIZE_CHARS", "900"))
CHUNK_OVERLAP_CHARS = int(os.getenv("CHUNK_OVERLAP_CHARS", "150"))
REQUEST_TIMEOUT_SEC = int(os.getenv("REQUEST_TIMEOUT_SEC", "60"))

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")
CHUNKS_PATH = os.path.join(DATA_DIR, "chunks.jsonl")
INDEX_PATH  = os.path.join(DATA_DIR, "faiss.index")
URL_LIST_PATH = os.path.join(DATA_DIR, "url_list.txt")