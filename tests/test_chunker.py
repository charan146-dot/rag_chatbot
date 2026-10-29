"""Test suite for Text Chunking stage."""

from pathlib import Path
from src.pdf_loader import extract_pages_from_pdf
from src.chunker import split_text_with_overlap, chunk_document_pages, clean_text_content


def test_clean_text_content():
    """Verify text cleaning removes excessive newlines and whitespace."""
    raw = "Line 1\r\n\r\n\r\n\r\nLine 2   \n\n\nLine 3"
    cleaned = clean_text_content(raw)
    assert "\r" not in cleaned
    assert "\n\n\n" not in cleaned
    assert "Line 1" in cleaned and "Line 3" in cleaned
    print("[PASS] test_clean_text_content")


def test_split_text_short():
    """Verify short text under chunk_size produces exactly one chunk."""
    short_text = "This is a concise paragraph of college lecture notes under 500 characters."
    chunks = split_text_with_overlap(short_text, chunk_size=500, chunk_overlap=100)
    assert len(chunks) == 1
    assert chunks[0]["text"] == short_text
    assert chunks[0]["start_char"] == 0
    assert chunks[0]["end_char"] == len(short_text)
    print("[PASS] test_split_text_short")


def test_split_text_overlap():
    """Verify long text produces multiple chunks with proper overlap."""
    # Create 1200 character dummy text
    sentence = "Data structures and algorithms form the core foundation of computer science. "
    long_text = sentence * 16  # ~1232 characters
    chunk_size = 500
    chunk_overlap = 100

    chunks = split_text_with_overlap(long_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    assert len(chunks) >= 3, f"Expected at least 3 chunks, got {len(chunks)}"

    # Check each chunk is approximately chunk_size
    for i, c in enumerate(chunks):
        assert len(c["text"]) <= chunk_size + 20, f"Chunk {i} exceeded expected size: {len(c['text'])}"

    # Check overlap between consecutive chunks:
    # The end of chunk 0 should share text with the beginning of chunk 1
    c0_tail = chunks[0]["text"][-50:]
    c1_head = chunks[1]["text"][:150]
    # At least some overlapping words should exist
    assert any(word in c1_head for word in c0_tail.split() if len(word) > 4), "Expected overlap between chunk 0 and 1"

    print("[PASS] test_split_text_overlap")


def test_empty_and_whitespace_handling():
    """Verify empty or whitespace strings return empty lists without crashing."""
    assert split_text_with_overlap("") == []
    assert split_text_with_overlap("    \n\n   ") == []

    # Test empty pages in chunk_document_pages
    mock_pages = [
        {"page_number": 1, "text": "   ", "char_count": 0, "is_empty": True},
        {"page_number": 2, "text": "", "char_count": 0, "is_empty": True},
    ]
    res = chunk_document_pages(mock_pages, source_name="empty_test.pdf")
    assert res["total_chunks"] == 0
    assert res["chunks"] == []
    print("[PASS] test_empty_and_whitespace_handling")


def test_chunk_document_pages_with_sample_pdf():
    """Verify end-to-end extraction -> chunking on sample college notes PDF."""
    sample_path = Path(__file__).resolve().parent.parent / "data" / "sample_college_notes.pdf"
    assert sample_path.exists(), "Sample PDF not found!"

    with open(sample_path, "rb") as f:
        extraction = extract_pages_from_pdf(f)

    assert extraction["success"] is True

    chunk_result = chunk_document_pages(
        pages=extraction["pages"],
        source_name="sample_college_notes.pdf",
        chunk_size=500,
        chunk_overlap=100
    )

    assert chunk_result["total_chunks"] > 0
    assert chunk_result["source_name"] == "sample_college_notes.pdf"

    # Check chunk identifiers & metadata
    chunk_ids = [c["chunk_id"] for c in chunk_result["chunks"]]
    # All IDs must be unique
    assert len(chunk_ids) == len(set(chunk_ids)), "Duplicate chunk IDs found!"

    for c in chunk_result["chunks"]:
        assert "chunk_id" in c
        assert "text" in c
        assert c["char_count"] > 0
        assert "metadata" in c
        meta = c["metadata"]
        assert meta["source"] == "sample_college_notes.pdf"
        assert meta["page_number"] in [1, 2]  # Page 3 was empty!
        assert "start_char" in meta
        assert "end_char" in meta

    # Ensure page 3 produced no chunks
    page_numbers_in_chunks = [c["metadata"]["page_number"] for c in chunk_result["chunks"]]
    assert 3 not in page_numbers_in_chunks, "Empty page 3 should not produce chunks!"

    print("[PASS] test_chunk_document_pages_with_sample_pdf")


if __name__ == "__main__":
    print("Running Text Chunker Test Suite...")
    test_clean_text_content()
    test_split_text_short()
    test_split_text_overlap()
    test_empty_and_whitespace_handling()
    test_chunk_document_pages_with_sample_pdf()
    print("ALL CHUNKER TESTS PASSED SUCCESSFULLY!")

