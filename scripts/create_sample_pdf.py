"""Generate sample PDF with exact xref table byte offsets."""

from pathlib import Path


def create_sample_college_notes(output_path: Path):
    """Write a clean, standards-compliant multi-page PDF with college lecture text."""
    body_parts = [
        b"%PDF-1.4\n",
        # Obj 1: Catalog
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        # Obj 2: Pages root (3 pages)
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R 4 0 R 5 0 R] /Count 3 >>\nendobj\n",
        # Obj 3: Page 1
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 6 0 R /Resources << /Font << /F1 7 0 R >> >> >>\nendobj\n",
        # Obj 4: Page 2
        b"4 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 8 0 R /Resources << /Font << /F1 7 0 R >> >> >>\nendobj\n",
        # Obj 5: Page 3 (Empty page)
        b"5 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 7 0 R >> >> >>\nendobj\n",
        # Obj 6: Content for Page 1
        b"6 0 obj\n<< /Length 174 >>\nstream\nBT\n/F1 18 Tf\n50 720 Td\n(CS 101: Introduction to Data Structures) Tj\n/F1 12 Tf\n0 -30 Td\n(Lecture 1: Arrays and Linked Lists.) Tj\n0 -20 Td\n(Arrays provide O(1) random access by index.) Tj\nET\nendstream\nendobj\n",
        # Obj 7: Font
        b"7 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
        # Obj 8: Content for Page 2
        b"8 0 obj\n<< /Length 165 >>\nstream\nBT\n/F1 14 Tf\n50 720 Td\n(Lecture 2: Hash Tables and Collision Handling) Tj\n/F1 12 Tf\n0 -30 Td\n(Separate chaining uses linked lists for bucket collisions.) Tj\nET\nendstream\nendobj\n",
    ]

    # Calculate exact byte offsets for objects 1 through 8
    offsets = [0]
    current_len = len(body_parts[0])
    for part in body_parts[1:]:
        offsets.append(current_len)
        current_len += len(part)

    xref_offset = current_len

    xref = [f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode("ascii")]
    for off in offsets[1:]:
        xref.append(f"{off:010d} 00000 n \n".encode("ascii"))

    trailer = f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")

    full_pdf = b"".join(body_parts) + b"".join(xref) + trailer

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(full_pdf)
    print(f"Generated clean sample PDF: {output_path}")


if __name__ == "__main__":
    target = Path(__file__).resolve().parent.parent / "data" / "sample_college_notes.pdf"
    create_sample_college_notes(target)
