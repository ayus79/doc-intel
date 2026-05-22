import ollama
from core.config import settings
from core.embedder import embed_query
from core.vector_db_client import qdrant_obj
from core.constants import RAG_MIN_SCORE, RAG_SYSTEM_PROMPT


def answer_query(question: str) -> dict:
    query_vec = embed_query(question)
    chunks = [
        c
        for c in qdrant_obj.search(
            settings.collection_name, query_vec, top_k=settings.top_k
        )
        if c["score"] >= RAG_MIN_SCORE
    ]

    if not chunks:
        return {
            "answer": "No relevant information found in the uploaded documents.",
            "sources": [],
        }

    context = "\n\n".join(
        f"[{i+1}] (Doc: {c['doc_name']}, Page: {c['page_number']})\n{c['text']}"
        for i, c in enumerate(chunks)
    )

    response = ollama.chat(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        options={"temperature": 0.1},
    )

    sources = [
        {
            "doc_name": c["doc_name"],
            "page_number": c["page_number"],
            "score": c["score"],
        }
        for c in chunks
    ]

    return {"answer": response.message.content, "sources": sources}
