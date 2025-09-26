from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.indexer import load_index_and_chunks
from app.retriever import cosine_topk
from app.rag import answer_question

app = FastAPI(title="SupportSolutions RAG API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskReq(BaseModel):
    question: str
    language: str = "da"  # Default to Danish

INDEX, CHUNKS = load_index_and_chunks()

@app.post("/ask")
def ask(req: AskReq):
    docs, _ = cosine_topk(INDEX, CHUNKS, req.question, k=6)
    out = answer_question(req.question, docs, req.language)
    return out