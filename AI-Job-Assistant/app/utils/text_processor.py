import re


def clean_text(text: str) -> str:
    # Replace tabs and multiple spaces with one space
    text = re.sub(r"\s+", " ", text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks