"""PDF Loader Module.

Responsible for loading PDF documents and extracting text page-by-page using PyPDF,
preserving page numbers and handling errors, empty pages, and scanned documents.
"""

import io
from typing import Dict, Any, List
from pypdf import PdfReader
from pypdf.errors import PdfReadError, EmptyFileError


def extract_pages_from_pdf(pdf_source) -> Dict[str, Any]:
    """Extract text page-by-page from a PDF file while preserving page numbers.

    Args:
        pdf_source: A file path, bytes, or file-like object (such as Streamlit UploadedFile).

    Returns:
        Dict[str, Any]: Extraction summary containing:
            - success (bool): True if reading succeeded without fatal errors.
            - total_pages (int): Total number of pages detected.
            - pages (List[Dict[str, Any]]): List of dicts with page_number, text, char_count, is_empty.
            - readable_pages (int): Count of pages with non-whitespace text.
            - empty_pages (int): Count of empty pages.
            - total_characters (int): Sum of extracted character counts.
            - is_scanned_or_empty (bool): True if no readable text could be found across all pages.
            - warning (str | None): Explanatory warning (e.g., OCR recommendation if scanned).
            - error (str | None): Detailed error description if extraction failed.
    """
    result: Dict[str, Any] = {
        "success": False,
        "total_pages": 0,
        "pages": [],
        "readable_pages": 0,
        "empty_pages": 0,
        "total_characters": 0,
        "is_scanned_or_empty": False,
        "warning": None,
        "error": None,
    }

    try:
        # Handle Streamlit UploadedFile or file-like stream
        if hasattr(pdf_source, "seek"):
            pdf_source.seek(0)

        if hasattr(pdf_source, "getvalue"):
            stream = io.BytesIO(pdf_source.getvalue())
        elif isinstance(pdf_source, bytes):
            stream = io.BytesIO(pdf_source)
        else:
            stream = pdf_source

        reader = PdfReader(stream)

        # Check if PDF is encrypted
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                result["error"] = "The uploaded PDF is password-protected and cannot be read."
                return result

        total_pages = len(reader.pages)
        result["total_pages"] = total_pages

        if total_pages == 0:
            result["success"] = True
            result["is_scanned_or_empty"] = True
            result["warning"] = "The PDF file contains 0 pages."
            return result

        extracted_pages: List[Dict[str, Any]] = []
        total_chars = 0
        readable_count = 0
        empty_count = 0

        for idx, page in enumerate(reader.pages):
            page_num = idx + 1
            try:
                raw_text = page.extract_text() or ""
            except Exception:
                raw_text = ""

            clean_text = raw_text.strip()
            char_count = len(clean_text)
            is_empty = (char_count == 0)

            if is_empty:
                empty_count += 1
            else:
                readable_count += 1
                total_chars += char_count

            extracted_pages.append({
                "page_number": page_num,
                "text": raw_text,
                "char_count": char_count,
                "is_empty": is_empty,
            })

        result["pages"] = extracted_pages
        result["readable_pages"] = readable_count
        result["empty_pages"] = empty_count
        result["total_characters"] = total_chars
        result["success"] = True

        # Check for scanned or textless PDFs
        if total_chars == 0:
            result["is_scanned_or_empty"] = True
            result["warning"] = (
                "No readable text could be extracted from this PDF. "
                "The document may consist of scanned images or rasterized pages, "
                "which standard text extractors cannot read and would require Optical Character Recognition (OCR)."
            )
        elif empty_count > 0:
            result["warning"] = (
                f"{empty_count} of {total_pages} page(s) appear to be empty or contain non-extractable content (such as diagrams or images)."
            )

        return result

    except EmptyFileError:
        result["error"] = "The uploaded file is empty (0 bytes)."
        return result
    except PdfReadError as e:
        result["error"] = f"PyPDF was unable to parse this PDF file. It may be corrupted or malformed. Details: {str(e)}"
        return result
    except Exception as e:
        result["error"] = f"An unexpected error occurred while reading the PDF: {str(e)}"
        return result

