"""Test suite for PDF extraction stage."""

import io
from pathlib import Path
from pypdf import PdfWriter
from src.pdf_loader import extract_pages_from_pdf
from src.document_processor import extract_text_from_pdf


def test_sample_college_notes_pdf():
    """Test extraction on 3-page college notes PDF with text and 1 empty page."""
    sample_path = Path(__file__).resolve().parent.parent / "data" / "sample_college_notes.pdf"
    assert sample_path.exists(), f"Sample PDF missing at {sample_path}"

    with open(sample_path, "rb") as f:
        result = extract_pages_from_pdf(f)

    assert result["success"] is True, f"Extraction failed: {result['error']}"
    assert result["total_pages"] == 3, f"Expected 3 pages, got {result['total_pages']}"
    assert result["readable_pages"] == 2, f"Expected 2 readable pages, got {result['readable_pages']}"
    assert result["empty_pages"] == 1, f"Expected 1 empty page, got {result['empty_pages']}"
    assert result["total_characters"] > 0, "Expected non-zero character count"

    # Verify Page 1
    p1 = result["pages"][0]
    assert p1["page_number"] == 1
    assert "CS 101" in p1["text"], f"Missing 'CS 101' in page 1: {p1['text']}"
    assert p1["is_empty"] is False

    # Verify Page 2
    p2 = result["pages"][1]
    assert p2["page_number"] == 2
    assert "Hash Tables" in p2["text"], f"Missing 'Hash Tables' in page 2: {p2['text']}"
    assert p2["is_empty"] is False

    # Verify Page 3 (Empty)
    p3 = result["pages"][2]
    assert p3["page_number"] == 3
    assert p3["is_empty"] is True

    print("[PASS] test_sample_college_notes_pdf")


def test_scanned_or_empty_pdf():
    """Test handling of blank / scanned PDF where no text can be extracted."""
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)
    writer.add_blank_page(width=300, height=300)
    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)

    result = extract_pages_from_pdf(buf)

    assert result["success"] is True
    assert result["total_pages"] == 2
    assert result["readable_pages"] == 0
    assert result["empty_pages"] == 2
    assert result["is_scanned_or_empty"] is True
    assert "OCR" in result["warning"], f"Expected OCR guidance in warning: {result['warning']}"

    print("[PASS] test_scanned_or_empty_pdf")


def test_corrupt_pdf():
    """Test graceful error handling for corrupted / invalid PDF bytes."""
    corrupt_data = io.BytesIO(b"This is not a real PDF file at all.")
    result = extract_pages_from_pdf(corrupt_data)

    assert result["success"] is False
    assert result["error"] is not None
    assert "PyPDF was unable to parse" in result["error"] or "error" in result["error"].lower()

    print("[PASS] test_corrupt_pdf")


def test_document_processor_integration():
    """Test extract_text_from_pdf in document_processor module."""
    sample_path = Path(__file__).resolve().parent.parent / "data" / "sample_college_notes.pdf"
    with open(sample_path, "rb") as f:
        full_text = extract_text_from_pdf(f)

    assert "CS 101" in full_text
    assert "Hash Tables" in full_text
    print("[PASS] test_document_processor_integration")


if __name__ == "__main__":
    print("Running PDF Extraction Test Suite...")
    test_sample_college_notes_pdf()
    test_scanned_or_empty_pdf()
    test_corrupt_pdf()
    test_document_processor_integration()
    print("ALL TESTS PASSED SUCCESSFULLY!")
