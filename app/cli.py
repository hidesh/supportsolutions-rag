import sys
from app.indexer import load_index_and_chunks
from app.retriever import cosine_topk
from app.rag import answer_question

def main():
    index, chunks = load_index_and_chunks()
    print("RAG CLI – skriv dit spørgsmål (Ctrl+C for at stoppe)")
    while True:
        try:
            q = input("\n❓ > ").strip()
            if not q:
                continue
            docs, _ = cosine_topk(index, chunks, q, k=6)
            out = answer_question(q, docs)
            print("\n" + out["answer"])
            print("\nKilder:")
            for s in out["sources"]:
                print(f"{s['ref']} {s['title']} – {s['url']}")
        except KeyboardInterrupt:
            print("\nFarvel!")
            sys.exit(0)

if __name__ == "__main__":
    main()