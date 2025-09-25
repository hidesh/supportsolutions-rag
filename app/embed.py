import numpy as np
from typing import List
from openai import OpenAI
from .config import OPENAI_API_KEY, EMBED_MODEL, REQUEST_TIMEOUT_SEC

client = OpenAI(api_key=OPENAI_API_KEY)

def get_embeddings(texts: List[str]) -> List[List[float]]:
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts, timeout=REQUEST_TIMEOUT_SEC)
    return [d.embedding for d in resp.data]

def embed_vector(text: str) -> np.ndarray:
    v = get_embeddings([text])[0]
    return np.asarray(v, dtype="float32")