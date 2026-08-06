import os
import faiss
import numpy as np
from pathlib import Path
from src.utils.logger import get_logger
from src.utils.helpers import load_config
from rag.embed import Embedder
from src.utils.exceptions import RAGError

logger = get_logger(__name__)

def chunk_text(text, size=500, overlap=50):
    """Chunk text with overlap for RAG retrieval."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def ingest_documents():
    """Load docs, chunk them, embed, and build FAISS index."""
    try:
        config = load_config()
        docs_dir = Path(config["rag"]["rag_docs_dir"])
        index_path = Path(config["paths"]["faiss_index"])

        embedder = Embedder()

        all_chunks = []

        logger.info(f"Scanning documents in {docs_dir}...")

        for file in os.listdir(docs_dir):
            if file.endswith(".txt"):
                path = docs_dir / file
                text = path.read_text()

                chunks = chunk_text(
                    text,
                    size=config["rag"]["chunk_size"],
                    overlap=config["rag"]["chunk_overlap"]
                )
                all_chunks.extend(chunks)

        logger.info(f"Total chunks: {len(all_chunks)}")

        # Embed chunks
        vectors = embedder.embed(all_chunks).astype("float32")

        backend = os.getenv("VECTORSTORE_BACKEND", "faiss").strip().lower()
        if backend == "pinecone":
            from rag.pinecone_store import upsert_chunks

            upsert_chunks(all_chunks, vectors)
            logger.info("Pinecone index updated")
            return all_chunks, None
        if backend != "faiss":
            raise RAGError("VECTORSTORE_BACKEND must be 'faiss' or 'pinecone'.")

        # Build FAISS index
        dim = vectors.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(vectors)

        faiss.write_index(index, str(index_path))
        logger.info(f"FAISS index saved at {index_path}")

        return all_chunks, index

    except Exception as e:
        raise RAGError(f"Ingestion failed: {e}")
