from app.services.qdrant_service import QdrantService


def main():
    print("Connecting to Qdrant...")

    qdrant = QdrantService()

    assert qdrant.health_check(), "Qdrant connection failed"

    print("Qdrant connection: OK")

    qdrant.create_collection(vector_size=384)

    print("Collection creation: OK")

    assert qdrant.collection_exists(), "Qdrant collection was not created"

    print("Collection exists: OK")
    print("Collection name:", qdrant.collection_name)

    print("\nSTEP 4.9 TEST PASSED")


if __name__ == "__main__":
    main()