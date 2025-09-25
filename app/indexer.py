import os, orjson, json, faiss, numpy as np
from typing import List, Dict
from .config import DATA_DIR, CHUNKS_PATH, INDEX_PATH, URL_LIST_PATH, CHUNK_SIZE_CHARS, CHUNK_OVERLAP_CHARS
from .text_utils import clean_html_to_text, chunk_text
from .ingest_web import fetch_html, extract_main_content
from .embed import get_embeddings

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_urls() -> List[str]:
    if not os.path.exists(URL_LIST_PATH):
        return []
    with open(URL_LIST_PATH, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]

def build_chunks_from_urls(urls: List[str]) -> List[Dict]:
    records = []
    for url in urls:
        try:
            html = fetch_html(url)
            raw_text = extract_main_content(html)
            text = clean_html_to_text(raw_text)
            if not text or len(text) < 200:
                continue
            pieces = chunk_text(text, CHUNK_SIZE_CHARS, CHUNK_OVERLAP_CHARS)
            for i, chunk in enumerate(pieces):
                records.append({"url": url, "title": url, "chunk_id": i, "chunk": chunk})
        except Exception as e:
            print(f"[WARN] Could not ingest {url}: {e}")
    return records

def save_chunks_jsonl(records: List[Dict]):
    with open(CHUNKS_PATH, "wb") as f:
        for rec in records:
            f.write(orjson.dumps(rec))
            f.write(b"\n")

def load_chunks_jsonl() -> List[Dict]:
    if not os.path.exists(CHUNKS_PATH): return []
    out = []
    with open(CHUNKS_PATH, "rb") as f:
        for line in f:
            if line.strip():
                out.append(orjson.loads(line))
    return out

def build_faiss_index(records: List[Dict]):
    texts = [r["chunk"] for r in records]
    embs = get_embeddings(texts)
    arr = np.asarray(embs, dtype="float32")
    dim = arr.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(arr)
    faiss.write_index(index, INDEX_PATH)
    print(f"[OK] Saved FAISS index at {INDEX_PATH} with {arr.shape[0]} vectors")

def build_all():
    ensure_data_dir()
    urls = load_urls()
    print(f"[INFO] URLs: {len(urls)}")
    records = build_chunks_from_urls(urls)
    print(f"[INFO] Chunks: {len(records)}")
    save_chunks_jsonl(records)
    if records:
        build_faiss_index(records)
    else:
        print("[WARN] No records, index not built.")

def load_index_and_chunks():
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError("FAISS index not found. Run index build first.")
    index = faiss.read_index(INDEX_PATH)
    chunks = load_chunks_jsonl()
    return index, chunks