from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


def main():
    print("Loading embedding model...")

    embedding_service = EmbeddingService()

    print("Model:", embedding_service.model_name)
    print("Vector size:", embedding_service.vector_size)

    assert embedding_service.vector_size == 384

    skill = "Python"

    print(f"Generating embedding for: {skill}")

    vector = embedding_service.generate_embedding(skill)

    print("Embedding generated")
    print("Embedding length:", len(vector))

    qdrant = QdrantService()

    print("Storing skill in Qdrant...")

    qdrant.upsert_skill(
        point_id=1,
        skill=skill,
        vector=vector,
        metadata={
            "source": "test",
        },
    )

    print("Skill stored in Qdrant")

    print("Searching similar skills...")

    results = qdrant.search_similar_skills(
        query_vector=vector,
        limit=5,
    )

    print("Search results:")

    for result in results:
        print(result)

    assert len(results) > 0

    print("\nSTEP 4.10 TEST PASSED")


if __name__ == "__main__":
    main()