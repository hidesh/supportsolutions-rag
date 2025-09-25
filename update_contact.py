#!/usr/bin/env python3

"""Quick script to update just the contact page chunks"""

import sys
import os
sys.path.append('.')

from app.indexer import load_chunks_jsonl, save_chunks_jsonl, build_faiss_index
from app.ingest_web import fetch_html, extract_main_content
from app.text_utils import clean_html_to_text, chunk_text
from app.config import CHUNK_SIZE_CHARS, CHUNK_OVERLAP_CHARS

def update_contact_info():
    # Load existing chunks
    records = load_chunks_jsonl()
    print(f"Loaded {len(records)} existing chunks")
    
    # Remove old contact page chunks
    records = [r for r in records if 'kontakt' not in r['url']]
    print(f"After removing contact chunks: {len(records)} chunks")
    
    # Fetch and process contact page
    try:
        html = fetch_html("https://support-solutions.dk/kontakt/")
        raw_text = extract_main_content(html)
        text = clean_html_to_text(raw_text)
        print(f"Contact page text: {text[:200]}...")
        
        pieces = chunk_text(text, CHUNK_SIZE_CHARS, CHUNK_OVERLAP_CHARS)
        for i, chunk in enumerate(pieces):
            records.append({
                "url": "https://support-solutions.dk/kontakt/", 
                "title": "https://support-solutions.dk/kontakt/", 
                "chunk_id": i, 
                "chunk": chunk
            })
        print(f"Added {len(pieces)} new contact chunks")
    except Exception as e:
        print(f"Error processing contact page: {e}")
    
    # Save updated chunks
    save_chunks_jsonl(records)
    print(f"Saved {len(records)} total chunks")
    
    # Rebuild index
    if records:
        build_faiss_index(records)
        print("Rebuilt FAISS index")

if __name__ == "__main__":
    update_contact_info()