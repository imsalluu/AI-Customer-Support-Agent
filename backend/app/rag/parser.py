import io
import re
from typing import List, Tuple

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None


class DocumentParser:
    @staticmethod
    def parse_pdf(file_bytes: bytes) -> List[Tuple[str, int, str]]:
        """Extracts text pages from PDF bytes. Returns list of (page_text, page_number, section_title)."""
        results = []
        if pypdf is not None:
            try:
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                for idx, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    text = text.strip()
                    if text:
                        first_line = text.split("\n")[0][:80]
                        results.append((text, idx + 1, first_line))
            except Exception:
                pass

        if not results:
            # Fallback raw extraction
            text_str = file_bytes.decode("utf-8", errors="ignore")
            results = DocumentParser.parse_text(text_str)

        return results

    @staticmethod
    def parse_docx(file_bytes: bytes) -> List[Tuple[str, int, str]]:
        """Extracts text from DOCX bytes. Returns list of (paragraph_text, page_estimate, section_title)."""
        results = []
        if docx is not None:
            try:
                doc = docx.Document(io.BytesIO(file_bytes))
                current_section = "General"
                buffer = []
                for p in doc.paragraphs:
                    text = p.text.strip()
                    if not text:
                        continue
                    if p.style.name.startswith("Heading"):
                        if buffer:
                            results.append(("\n".join(buffer), 1, current_section))
                            buffer = []
                        current_section = text
                    else:
                        buffer.append(text)

                if buffer:
                    results.append(("\n".join(buffer), 1, current_section))
            except Exception:
                pass

        if not results:
            text_str = file_bytes.decode("utf-8", errors="ignore")
            results = DocumentParser.parse_text(text_str)

        return results

    @staticmethod
    def parse_text(text_content: str) -> List[Tuple[str, int, str]]:
        """Extracts text from TXT or Markdown content with section headers."""
        results = []
        lines = text_content.split("\n")
        current_section = "Overview"
        buffer = []
        page_est = 1

        for line in lines:
            line_str = line.strip()
            if line_str.startswith("#"):
                if buffer:
                    results.append(("\n".join(buffer), page_est, current_section))
                    buffer = []
                current_section = line_str.lstrip("#").strip()
            elif line_str:
                buffer.append(line_str)

        if buffer:
            results.append(("\n".join(buffer), page_est, current_section))

        if not results and text_content.strip():
            results.append((text_content.strip(), 1, "General"))

        return results
