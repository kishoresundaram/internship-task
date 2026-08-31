import chromadb

from langchain_huggingface import HuggingFaceEmbeddings


# Create ChromaDB client
client = chromadb.PersistentClient(
    path="data/chroma"
)


# Create embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Create or get collection
collection = client.get_or_create_collection(
    name="job_descriptions"
)


def store_chunks(chunks, filename):
    """
    Convert JD chunks into embeddings
    and store them in ChromaDB.
    """

    documents = chunks

    ids = [
        f"{filename}_{index}"
        for index in range(len(chunks))
    ]

    # Generate embeddings
    embeddings_list = embeddings.embed_documents(documents)

    # Store documents and embeddings
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings_list,
        metadatas=[
            {"filename": filename}
            for _ in chunks
        ]
    )

    return len(chunks)


def search_similar_chunks(query, top_k=3):
    """
    Search ChromaDB for chunks
    similar to the user's question.
    """

    query_embedding = embeddings.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results