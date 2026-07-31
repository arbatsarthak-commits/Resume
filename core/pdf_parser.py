import fitz  # PyMuPDF
from typing import Tuple, Dict, Any

def parse_pdf(file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
    """
    Parses a PDF file from bytes.
    Returns (extracted_text, metadata_dict).
    Raises ValueError on corrupt or scanned PDFs without readable text.
    """
    if not file_bytes:
        raise ValueError("Provided PDF file is empty.")

    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Invalid or corrupted PDF file: {str(e)}")

    page_count = len(doc)
    if page_count == 0:
        raise ValueError("PDF file contains no pages.")

    full_text_pages = []
    total_text_length = 0

    for page_num in range(page_count):
        page = doc[page_num]
        page_text = page.get_text("text")
        full_text_pages.append(page_text)
        total_text_length += len(page_text.strip())

    combined_text = "\n\n".join(full_text_pages).strip()

    # Check for image-based/scanned PDF without selectable text
    if total_text_length < 30:
        raise ValueError("Text could not be reliably extracted. The resume may be image-based or scanned.")

    metadata = {
        "page_count": page_count,
        "character_count": total_text_length,
        "is_scanned": False
    }

    return combined_text, metadata
