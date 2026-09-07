from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.qdrant_config import (
    QDRANT_COLLECTION_NAME,
    get_qdrant_client,
)


class QdrantService:
    def __init__(
        self,
        collection_name: str = QDRANT_COLLECTION_NAME,
    ):
        self.client: QdrantClient = get_qdrant_client()
        self.collection_name = collection_name

    def health_check(self) -> bool:
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False

    def collection_exists(self) -> bool:
        return self.client.collection_exists(
            collection_name=self.collection_name
        )

    def create_collection(
        self,
        vector_size: int = 384,
    ) -> None:
        if self.collection_exists():
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert_skill(
        self,
        point_id: int,
        skill: str,
        vector: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        payload = {
            "skill": skill,
            "type": "skill",
        }

        if metadata:
            payload.update(metadata)

        point = PointStruct(
            id=point_id,
            vector=vector,
            payload=payload,
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
            wait=True,
        )

    def search_similar_skills(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )

        return results.points