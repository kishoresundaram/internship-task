import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
QDRANT_COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION_NAME",
    "recruitment_skills",
)


def get_qdrant_client() -> QdrantClient:
    if not QDRANT_URL:
        raise RuntimeError(
            "QDRANT_URL is not configured in the .env file"
        )

    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY or None,
    )