"""Optional Pinecone storage for the educational RAG path.

FAISS remains the default backend. This module is imported only when
VECTORSTORE_BACKEND=pinecone.
"""

from __future__ import annotations

import os
from typing import Iterable


def _config() -> tuple[str, str]:
    api_key = os.getenv("PINECONE_API_KEY", "").strip()
    index_name = os.getenv("PINECONE_INDEX_NAME", "").strip()
    namespace = os.getenv("PINECONE_NAMESPACE", "disease-capstone").strip()

    if not api_key:
        raise RuntimeError(
            "PINECONE_API_KEY is required when VECTORSTORE_BACKEND=pinecone."
        )
    if not index_name:
        raise RuntimeError(
            "PINECONE_INDEX_NAME is required when VECTORSTORE_BACKEND=pinecone."
        )
    if not namespace:
        raise RuntimeError("PINECONE_NAMESPACE must not be empty.")

    return index_name, namespace


def _index():
    from pinecone import Pinecone

    index_name, _ = _config()
    return Pinecone(api_key=os.environ["PINECONE_API_KEY"]).Index(index_name)


def upsert_chunks(chunks: Iterable[str], vectors) -> None:
    """Upsert embedded document chunks with source text metadata."""
    _, namespace = _config()
    records = [
        {
            "id": f"disease-capstone-{i}",
            "values": vector.tolist(),
            "metadata": {"text": text},
        }
        for i, (text, vector) in enumerate(zip(chunks, vectors, strict=True))
    ]
    _index().upsert(vectors=records, namespace=namespace)


def query_chunks(vector, top_k: int) -> list[str]:
    """Query Pinecone and return source text in score order."""
    _, namespace = _config()
    response = _index().query(
        vector=vector.tolist(),
        top_k=top_k,
        include_metadata=True,
        namespace=namespace,
    )
    return [
        match.metadata.get("text", "")
        for match in response.matches
        if match.metadata and match.metadata.get("text")
    ]
