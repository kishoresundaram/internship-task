
from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.search import router as search_router
from app.api.rag import router as rag_router
from app.api.auth import router as auth_router
from app.api.voice import router as voice_router

from app.database.database import create_tables


app = FastAPI(
    title="AI Job Assistant",
    description="Real-Time AI Job Assistant with Persistent Memory",
    version="1.0.0"
)


# Create database tablesgfd0
create_tables()


# Chat API
app.include_router(
    chat_router
)


# Document APIs
app.include_router(
    documents_router,
    prefix="/documents",
    tags=["Documents"]
)


# Search APIs
app.include_router(
    search_router,
    prefix="/search",
    tags=["Search"]
)


# RAG APIs
app.include_router(
    rag_router,
    prefix="/rag",
    tags=["RAG"]
)


# Authentication APIs
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)


# Voice APIs
app.include_router(
    voice_router,
    prefix="/voice",
    tags=["Voice"]
)


@app.get("/")
def home():

    return {
        "message": "AI Job Assistant API is running"
    }

