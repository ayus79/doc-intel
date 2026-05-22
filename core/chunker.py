from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.parser import ParsedPage
from core.config import settings
from dataclasses import dataclass


@dataclass
class Chunk:
    doc_name: str
    page_number: int
    text: str


def chunk_pages(pages: list[ParsedPage]) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = []
    for page in pages:
        splits = splitter.split_text(page.text)
        for split in splits:
            chunks.append(
                Chunk(
                    doc_name=page.doc_name,
                    page_number=page.page_number,
                    text=split,
                )
            )
    return chunks
