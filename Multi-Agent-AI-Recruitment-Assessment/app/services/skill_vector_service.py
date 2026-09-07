from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class SkillVectorService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def store_skills(
        self,
        skills: list[str],
        source: str,
        candidate_id: int | None = None,
        job_description_id: int | None = None,
    ) -> None:
        if not skills:
            return

        embeddings = self.embedding_service.generate_embeddings(skills)

        for index, (skill, vector) in enumerate(
            zip(skills, embeddings)
        ):
            point_id = abs(hash(
                f"{source}:{candidate_id}:{job_description_id}:{skill}:{index}"
            ))

            metadata = {
                "source": source,
            }

            if candidate_id is not None:
                metadata["candidate_id"] = candidate_id

            if job_description_id is not None:
                metadata["job_description_id"] = job_description_id

            self.qdrant_service.upsert_skill(
                point_id=point_id,
                skill=skill,
                vector=vector,
                metadata=metadata,
            )

    def search_skills(
        self,
        skill: str,
        limit: int = 5,
    ):
        query_vector = self.embedding_service.generate_embedding(
            skill
        )

        return self.qdrant_service.search_similar_skills(
            query_vector=query_vector,
            limit=limit,
        )