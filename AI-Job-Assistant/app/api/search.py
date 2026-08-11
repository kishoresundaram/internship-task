from fastapi import APIRouter

from app.utils.vector_store import search_similar_chunks


router = APIRouter()


@router.get("/search")
def search_job_description(query: str, top_k: int = 3):

    results = search_similar_chunks(
        query=query,
        top_k=top_k
    )

    return {
        "query": query,
        "results": results
    }