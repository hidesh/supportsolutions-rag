import re
from typing import List

def clean_html_to_text(html: str) -> str:
    html = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;?", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> List[str]:
    chunks = []
    i, n = 0, len(text)
    while i < n:
        end = min(i + chunk_size, n)
        piece = text[i:end]
        if end < n:
            last_dot = piece.rfind(".")
            if last_dot > int(chunk_size * 0.6):
                piece = piece[:last_dot+1]
        piece = piece.strip()
        if piece:
            chunks.append(piece)
        i += max(len(piece) - overlap, 1)
    return chunks