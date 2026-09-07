import fitz


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF resume.
    """

    document = fitz.open(file_path)

    text_parts = []

    for page in document:
        page_text = page.get_text()

        if page_text:
            text_parts.append(page_text)

    document.close()

    extracted_text = "\n".join(text_parts)

    return extracted_text.strip()


def clean_resume_text(text: str) -> str:
    """
    Clean extracted resume text.
    """

    lines = []

    for line in text.splitlines():
        cleaned_line = " ".join(line.split())

        if cleaned_line:
            lines.append(cleaned_line)

    return "\n".join(lines)