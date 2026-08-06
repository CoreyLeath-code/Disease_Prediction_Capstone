import faiss
from openai import OpenAI
from pathlib import Path
from rag.embed import Embedder
from src.utils.helpers import load_config
from src.utils.logger import get_logger
from src.utils.exceptions import RAGError

logger = get_logger(__name__)

def rag_query(user_question: str):
    """Return relevant medical text + LLM-generated explanation."""
    try:
        config = load_config()

        backend = os.getenv("VECTORSTORE_BACKEND", "faiss").strip().lower()
        if backend not in {"faiss", "pinecone"}:
            raise RAGError("VECTORSTORE_BACKEND must be 'faiss' or 'pinecone'.")

        index = None
        if backend == "faiss":
            index_path = Path(config["paths"]["faiss_index"])
            index = faiss.read_index(str(index_path))

        # Load chunks
        docs_dir = Path(config["rag"]["rag_docs_dir"])
        chunks = []
        for f in docs_dir.iterdir():
            if f.suffix == ".txt":
                chunks.extend(f.read_text().split("\n"))

        # Embed question
        embedder = Embedder()
        q_vec = embedder.embed([user_question]).astype("float32")

        # Retrieve top-k
        k = config["rag"]["top_k"]
        if backend == "pinecone":
            from rag.pinecone_store import query_chunks

            retrieved_texts = query_chunks(q_vec[0], k)
        else:
            distances, indices = index.search(q_vec, k)
            retrieved_texts = [chunks[i] for i in indices[0]]

        # LLM Explanation
        client = OpenAI()
        prompt = f"""
        You are a medical assistant. Using the medical reference text below,
        answer the following question with accuracy and clarity.

        QUESTION:
        {user_question}

        RELEVANT TEXT:
        {' '.join(retrieved_texts)}

        Provide a helpful explanation.
        """

        response = client.chat.completions.create(
            model=config["llm"]["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=config["llm"]["temperature"],
            max_tokens=config["llm"]["max_tokens"]
        )

        answer = response.choices[0].message.content
        return {
            "answer": answer,
            "sources": retrieved_texts
        }

    except Exception as e:
        raise RAGError(f"RAG query failed: {e}")
