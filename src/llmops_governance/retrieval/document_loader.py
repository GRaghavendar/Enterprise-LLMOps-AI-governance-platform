"""Markdown policy document loader."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class PolicyDocument:
    source_document: str
    path: Path
    text: str


def load_markdown_documents(directory: Path) -> list[PolicyDocument]:
    documents: list[PolicyDocument] = []
    if not directory.exists():
        return documents
    for path in sorted(directory.glob("*.md")):
        documents.append(PolicyDocument(source_document=path.name, path=path, text=path.read_text(encoding="utf-8")))
    return documents

