"""Simple markdown chunking for deterministic local retrieval."""

from __future__ import annotations

from llmops_governance.retrieval.document_loader import PolicyDocument
from llmops_governance.schemas.evaluation import SourceChunk
from llmops_governance.utils import stable_id


def chunk_document(document: PolicyDocument, max_words: int = 120) -> list[SourceChunk]:
    paragraphs = [part.strip() for part in document.text.split("\n\n") if part.strip()]
    chunks: list[SourceChunk] = []
    buffer: list[str] = []
    word_count = 0
    for paragraph in paragraphs:
        words = paragraph.split()
        if buffer and word_count + len(words) > max_words:
            text = "\n\n".join(buffer)
            chunks.append(
                SourceChunk(
                    chunk_id=stable_id(document.source_document, text, prefix="chunk"),
                    source_document=document.source_document,
                    text=text,
                    similarity_score=0.0,
                )
            )
            buffer = []
            word_count = 0
        buffer.append(paragraph)
        word_count += len(words)
    if buffer:
        text = "\n\n".join(buffer)
        chunks.append(
            SourceChunk(
                chunk_id=stable_id(document.source_document, text, prefix="chunk"),
                source_document=document.source_document,
                text=text,
                similarity_score=0.0,
            )
        )
    return chunks


def chunk_documents(documents: list[PolicyDocument], max_words: int = 120) -> list[SourceChunk]:
    chunks: list[SourceChunk] = []
    for document in documents:
        chunks.extend(chunk_document(document, max_words=max_words))
    return chunks

