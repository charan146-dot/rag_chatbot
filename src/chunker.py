"""Text Chunker Module.

Responsible for:
1. Splitting extracted PDF text into overlapping semantic chunks.
2. Preserving document metadata (source filename, original page number).
3. Assigning unique identifiers to every chunk for vector storage and retrieval citations.
4. Handling empty pages and whitespace cleanly without producing meaningless chunks.
"""

import re
from typing import List, Dict, Any
from pathlib import Path


def clean_text_content(text: str) -> str:
    """Standardize whitespace and remove excessive blank lines."""
    if not text:
        return ""
    # Replace carriage returns and excessive whitespace
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse multiple consecutive empty lines into two newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_text_with_overlap(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[Dict[str, Any]]:
    """Split a continuous text string into overlapping chunks.

    Tries to split on natural word or sentence boundaries near the chunk_size
    boundary rather than cutting in the middle of words.

    Args:
        text (str): Input text string.
        chunk_size (int): Target character size per chunk.
        chunk_overlap (int): Number of overlapping characters between consecutive chunks.

    Returns:
        List[Dict[str, Any]]: List of chunk segment dicts containing:
            - text (str): The chunk text.
            - start_char (int): Character start offset in the original string.
            - end_char (int): Character end offset in the original string.
    """
    clean_text = clean_text_content(text)
    if not clean_text:
        return []

    # Safeguard parameters
    if chunk_size <= 0:
        chunk_size = 500
    if chunk_overlap < 0:
        chunk_overlap = 0
    if chunk_overlap >= chunk_size:
        chunk_overlap = max(0, chunk_size - 50)

    total_len = len(clean_text)

    # If text is already smaller than or equal to target chunk size, return as a single chunk
    if total_len <= chunk_size:
        return [{
            "text": clean_text,
            "start_char": 0,
            "end_char": total_len,
        }]

    segments: List[Dict[str, Any]] = []
    start = 0

    while start < total_len:
        target_end = min(start + chunk_size, total_len)

        # If we have reached the end of text
        if target_end >= total_len:
            actual_end = total_len
        else:
            # Look backwards from target_end for a natural delimiter (newline, period, space)
            # Search within a 20% window backwards from target_end
            search_window_start = max(start + 50, target_end - int(chunk_size * 0.2))
            boundary_idx = -1

            # Priority 1: Paragraph break (newline)
            newline_pos = clean_text.rfind("\n", search_window_start, target_end)
            if newline_pos != -1:
                boundary_idx = newline_pos + 1
            else:
                # Priority 2: Sentence end (period + space)
                period_pos = clean_text.rfind(". ", search_window_start, target_end)
                if period_pos != -1:
                    boundary_idx = period_pos + 2
                else:
                    # Priority 3: Word boundary (space)
                    space_pos = clean_text.rfind(" ", search_window_start, target_end)
                    if space_pos != -1:
                        boundary_idx = space_pos + 1

            # If a natural boundary was found, break there; otherwise break at target_end
            actual_end = boundary_idx if boundary_idx != -1 else target_end

        chunk_str = clean_text[start:actual_end].strip()
        if chunk_str:
            segments.append({
                "text": chunk_str,
                "start_char": start,
                "end_char": actual_end,
            })

        if actual_end >= total_len:
            break

        # Calculate next start with overlap
        step = max(1, (actual_end - start) - chunk_overlap)
        start += step

    return segments


def chunk_document_pages(
    pages: List[Dict[str, Any]],
    source_name: str = "document.pdf",
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> Dict[str, Any]:
    """Chunk extracted document pages while preserving page metadata and unique IDs.

    Args:
        pages (List[Dict[str, Any]]): List of page records from extract_pages_from_pdf.
        source_name (str): Original filename of the uploaded PDF.
        chunk_size (int): Configurable chunk size in characters (~500).
        chunk_overlap (int): Configurable overlap in characters (~100).

    Returns:
        Dict[str, Any]: Summary dictionary containing:
            - chunks (List[Dict[str, Any]]): Processed chunk objects.
            - total_chunks (int): Total number of valid chunks generated.
            - total_characters (int): Sum of chunk characters.
            - avg_chunk_size (float): Average chunk length.
            - source_name (str): Document filename.
            - chunk_size (int): Configured chunk size.
            - chunk_overlap (int): Configured overlap.
    """
    clean_source = Path(source_name).name
    # Create a clean alphanumeric slug for prefixing chunk IDs
    slug = re.sub(r"[^a-zA-Z0-9_]", "_", Path(source_name).stem).lower()
    if not slug:
        slug = "doc"

    all_chunks: List[Dict[str, Any]] = []
    global_chunk_idx = 0

    for page_record in pages:
        page_num = page_record.get("page_number", 1)
        raw_text = page_record.get("text", "")
        is_empty = page_record.get("is_empty", False)

        # Skip empty pages or whitespace-only content cleanly
        if is_empty or not raw_text or not raw_text.strip():
            continue

        page_segments = split_text_with_overlap(
            text=raw_text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for page_chunk_idx, segment in enumerate(page_segments):
            chunk_id = f"{slug}_p{page_num}_c{page_chunk_idx}"
            chunk_text = segment["text"]
            char_count = len(chunk_text)

            all_chunks.append({
                "chunk_id": chunk_id,
                "global_index": global_chunk_idx,
                "text": chunk_text,
                "char_count": char_count,
                "metadata": {
                    "source": clean_source,
                    "page_number": page_num,
                    "chunk_index_in_page": page_chunk_idx,
                    "global_chunk_index": global_chunk_idx,
                    "start_char": segment["start_char"],
                    "end_char": segment["end_char"],
                    "chunk_size_configured": chunk_size,
                    "chunk_overlap_configured": chunk_overlap,
                }
            })
            global_chunk_idx += 1

    total_chunks = len(all_chunks)
    total_chars = sum(c["char_count"] for c in all_chunks)
    avg_size = round(total_chars / total_chunks, 1) if total_chunks > 0 else 0.0

    return {
        "chunks": all_chunks,
        "total_chunks": total_chunks,
        "total_characters": total_chars,
        "avg_chunk_size": avg_size,
        "source_name": clean_source,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
    }

