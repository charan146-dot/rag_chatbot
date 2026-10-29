"""Document Processor Module.

Coordinates:
1. Loading and extracting raw text from uploaded PDF notes (via src.pdf_loader).
2. Splitting extracted page text into overlapping chunks with metadata (via src.chunker).
"""

from typing import List, Dict, Any
from src.pdf_loader import extract_pages_from_pdf
from src.chunker import split_text_with_overlap, chunk_document_pages


def extract_text_from_pdf(pdf_file) -> str:
    """Extract raw combined text content from an uploaded PDF file.

    Args:
        pdf_file: Uploaded PDF file object (e.g., from Streamlit file_uploader).

    Returns:
        str: Raw text extracted across all pages.
    """
    extraction_result = extract_pages_from_pdf(pdf_file)
    if not extraction_result["success"]:
        error_msg = extraction_result.get("error") or "Unknown error reading PDF"
        raise ValueError(error_msg)

    # Combine text from all non-empty pages
    all_texts = [p["text"] for p in extraction_result["pages"] if not p["is_empty"]]
    return "\n\n".join(all_texts)


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[Dict[str, Any]]:
    """Split raw text into smaller overlapping chunks.

    Args:
        text (str): The raw text to split.
        chunk_size (int): Target character size for each chunk (~500).
        chunk_overlap (int): Number of overlapping characters (~100).

    Returns:
        List[Dict[str, Any]]: List of chunk dictionaries containing text, start_char, and end_char.
    """
    return split_text_with_overlap(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
