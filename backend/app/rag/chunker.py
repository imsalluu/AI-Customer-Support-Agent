import re
from typing import List, Optional
from pydantic import BaseModel


class ParsedChunk(BaseModel):
    content: str
    chunk_index: int
    page_number: Optional[int] = None
    section_title: Optional[str] = None
    token_count: int


class TextChunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(
        self,
        sections: List[tuple],  # [(text, page_number, section_title)]
    ) -> List[ParsedChunk]:
        """Splits extracted document sections into overlapping chunks."""
        chunks: List[ParsedChunk] = []
        chunk_idx = 0

        for text, page_num, section_title in sections:
            # Normalize whitespace
            clean_text = re.sub(r"\s+", " ", text).strip()
            if not clean_text:
                continue

            if len(clean_text) <= self.chunk_size:
                chunks.append(
                    ParsedChunk(
                        content=clean_text,
                        chunk_index=chunk_idx,
                        page_number=page_num,
                        section_title=section_title,
                        token_count=len(clean_text.split()),
                    )
                )
                chunk_idx += 1
                continue

            # Split with overlap
            start = 0
            while start < len(clean_text):
                end = min(start + self.chunk_size, len(clean_text))
                # Try to break at a sentence or word boundary
                if end < len(clean_text):
                    boundary = clean_text.rfind(". ", start, end)
                    if boundary != -1 and boundary > start + 100:
                        end = boundary + 1
                    else:
                        space = clean_text.rfind(" ", start, end)
                        if space != -1 and space > start + 100:
                            end = space

                chunk_text = clean_text[start:end].strip()
                if chunk_text:
                    chunks.append(
                        ParsedChunk(
                            content=chunk_text,
                            chunk_index=chunk_idx,
                            page_number=page_num,
                            section_title=section_title,
                            token_count=len(chunk_text.split()),
                        )
                    )
                    chunk_idx += 1

                if end >= len(clean_text):
                    break
                start = max(end - self.chunk_overlap, start + 1)

        return chunks
