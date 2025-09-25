import numpy as np
from typing import List, Dict, Tuple
from .embed import embed_vector
from .config import TOP_K

def expand_query(query: str) -> str:
    """Udvid søgeforespørgslen med synonymer og relevante termer."""
    expansions = {
        "support": ["support", "hjælp", "assistance", "service"],
        "cloud": ["cloud", "sky", "online", "hosted", "saas"],
        "it": ["it", "teknologi", "computer", "system"],
        "pris": ["pris", "kostnad", "cost", "price", "økonomi"],
        "backup": ["backup", "sikkerhedskopi", "restore"],
        "sikkerhed": ["sikkerhed", "security", "beskyttelse", "firewall"],
        "server": ["server", "hosting", "infrastruktur"],
        "konsulent": ["konsulent", "rådgiver", "ekspert", "specialist"]
    }
    
    query_lower = query.lower()
    expanded_terms = [query]
    
    for key, synonyms in expansions.items():
        if key in query_lower:
            expanded_terms.extend(synonyms)
    
    return " ".join(set(expanded_terms))

def cosine_topk(index, chunks: List[Dict], query: str, k: int = None) -> Tuple[List[Dict], List[float]]:
    if k is None: k = TOP_K
    
    # Udvid query for bedre søgeresultater
    expanded_query = expand_query(query)
    qv = embed_vector(expanded_query).reshape(1, -1)
    
    # Hent flere resultater end nødvendigt for re-ranking
    search_k = min(k * 2, len(chunks))
    D, I = index.search(qv, search_k)
    idxs = I[0].tolist()
    dists = D[0].tolist()
    
    scored = []
    for i, dist in zip(idxs, dists):
        if i < 0 or i >= len(chunks):
            continue
        # L2-dist -> score (negativ distance)
        score = -float(dist)
        
        # Boost score for chunks med nøgleord i titel eller url
        chunk_text = chunks[i].get('chunk', '').lower()
        chunk_url = chunks[i].get('url', '').lower()
        
        if 'support-solutions.dk' in chunk_url:
            score += 0.1  # Boost for hjemmeside chunks
            
        # Boost for query relevans
        query_words = query.lower().split()
        for word in query_words:
            if word in chunk_text:
                score += 0.05
                
        scored.append((chunks[i], score))
    
    if not scored:
        return [], []
        
    # Sortér efter score og tag top-k
    scored.sort(key=lambda x: x[1], reverse=True)
    top_scored = scored[:k]
    
    docs, scores = zip(*top_scored)
    return list(docs), list(scores)