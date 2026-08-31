import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()


# ============================================================
# Sentence Transformer Model
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# ============================================================
# Qdrant Configuration
# ============================================================

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)


COLLECTION_NAME = "resume_embeddings"


# ============================================================
# Generate Embedding
# ============================================================

def generate_embedding(text: str):
    """
    Convert text into a 384-dimensional vector.
    """

    embedding = model.encode(text)

    return embedding.tolist()


# ============================================================
# Create Qdrant Collection
# ============================================================

def create_collection():
    """
    Create the resume_embeddings collection
    if it does not already exist.
    """

    collections = client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in collection_names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


# ============================================================
# Store Resume Embedding
# ============================================================

def store_resume_embedding(
    resume_id: int,
    filename: str,
    text: str
):
    """
    Generate an embedding for a resume
    and store it in Qdrant.
    """

    embedding = generate_embedding(text)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=resume_id,
                vector=embedding,
                payload={
                    "resume_id": resume_id,
                    "filename": filename
                }
            )
        ]
    )

    return embedding


# ============================================================
# Search Similar Resumes
# ============================================================

def search_similar_resumes(
    job_description: str,
    limit: int = 5
):
    """
    Convert a job description into an embedding
    and search for the most similar resumes in Qdrant.
    """

    job_embedding = generate_embedding(job_description)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=job_embedding,
        limit=limit,
        with_payload=True
    )

    return results.points