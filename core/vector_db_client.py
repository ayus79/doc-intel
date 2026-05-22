import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from core.config import settings
from core.embedder import VECTOR_DIM


class QdrantStore:

    def __init__(self, host: str, port: int, vector_dim: int):
        self._client = QdrantClient(host=host, port=port)
        self._vector_dim = vector_dim

    # ---------- Collection ----------

    def ensure_collection(self, collection: str):
        existing = [c.name for c in self._client.get_collections().collections]
        if collection not in existing:
            self._client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(
                    size=self._vector_dim, distance=Distance.COSINE
                ),
            )

    def delete_collection(self, collection: str):
        self._client.delete_collection(collection)

    # ---------- Write ----------

    def upsert(self, collection: str, chunks, embeddings: list[list[float]]):
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "doc_name": chunk.doc_name,
                    "page_number": chunk.page_number,
                    "text": chunk.text,
                },
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]
        self._client.upsert(collection_name=collection, points=points)

    def delete_document(self, collection: str, doc_name: str):
        self._client.delete(
            collection_name=collection,
            points_selector=Filter(
                must=[FieldCondition(key="doc_name", match=MatchValue(value=doc_name))]
            ),
        )

    # ---------- Read ----------

    def search(
        self, collection: str, query_vector: list[float], top_k: int = 5
    ) -> list[dict]:
        results = self._client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
        )
        return [
            {
                "text": r.payload["text"],
                "doc_name": r.payload["doc_name"],
                "page_number": r.payload["page_number"],
                "score": r.score,
            }
            for r in results
        ]

    def _collection_exists(self, collection: str) -> bool:
        return collection in [
            c.name for c in self._client.get_collections().collections
        ]

    def list_documents(self, collection: str) -> list[str]:
        if not self._collection_exists(collection):
            return []
        seen, offset = set(), None
        while True:
            records, offset = self._client.scroll(
                collection_name=collection,
                limit=256,
                offset=offset,
                with_payload=["doc_name"],
            )
            for r in records:
                seen.add(r.payload["doc_name"])
            if offset is None:
                break
        return sorted(seen)

    def count(self, collection: str) -> int:
        if not self._collection_exists(collection):
            return 0
        return self._client.count(collection_name=collection).count

    def get_chunks_by_document(self, collection: str, doc_name: str) -> list[dict]:
        if not self._collection_exists(collection):
            return []
        records, _ = self._client.scroll(
            collection_name=collection,
            scroll_filter=Filter(
                must=[FieldCondition(key="doc_name", match=MatchValue(value=doc_name))]
            ),
            limit=500,
            with_payload=True,
            with_vectors=False,
        )
        return [
            {
                "page_number": r.payload["page_number"],
                "text": r.payload["text"],
            }
            for r in records
        ]


# Single instance - reuse across any collection
qdrant_obj = QdrantStore(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
    vector_dim=VECTOR_DIM,
)
