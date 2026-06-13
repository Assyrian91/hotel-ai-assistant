from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, analytics
from app.database import create_tables
from app.agents.rag_agent import build_vector_store
from app.config import FAISS_PATH
import os

app = FastAPI(title="AI Hotel Operations Assistant", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(chat.router)
app.include_router(analytics.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup():
    create_tables()
    if not os.path.exists(FAISS_PATH):
        print("Building vector store...")
        build_vector_store()

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}
