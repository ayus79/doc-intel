from fastapi import UploadFile
from core.rag import answer_query
from core.vector_db_client import qdrant_obj
from core.embedder import embed_texts
from core.config import settings
from core.parser import parser, SUPPORTED_FORMATS
from core.chunker import chunk_pages


async def upload_file(file: UploadFile) -> dict:
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in SUPPORTED_FORMATS:
        return {
            "status": False,
            "message": f"Unsupported format .{ext}. Supported: {sorted(SUPPORTED_FORMATS)}",
            "status_code": 400,
        }

    file_bytes = await file.read()
    pages = parser.parse(file_bytes, file.filename)

    if not pages:
        return {
            "status": False,
            "message": "No extractable text found in this file.",
            "status_code": 422,
        }

    chunks = chunk_pages(pages)
    embeddings = embed_texts([c.text for c in chunks])

    qdrant_obj.ensure_collection(settings.collection_name)
    qdrant_obj.upsert(settings.collection_name, chunks, embeddings)

    return {
        "status": True,
        "message": "File indexed successfully.",
        "data": {
            "doc_name": file.filename,
            "pages_parsed": len(pages),
            "chunks_stored": len(chunks),
        },
        "status_code": 201,
    }


def query_document(question: str) -> dict:
    if not question.strip():
        return {
            "status": False,
            "message": "Question cannot be empty.",
            "status_code": 400,
        }

    result = answer_query(question)
    return {
        "status": True,
        "message": "Query answered successfully.",
        "data": result,
        "status_code": 200,
    }


def get_documents() -> dict:
    docs = qdrant_obj.list_documents(settings.collection_name)
    return {
        "status": True,
        "message": "Documents fetched successfully.",
        "data": {"documents": docs},
        "status_code": 200,
    }


def get_doc_chunks(doc_name: str) -> dict:
    chunks = qdrant_obj.get_chunks_by_document(settings.collection_name, doc_name)
    return {
        "status": True,
        "message": "Chunks fetched successfully.",
        "data": {"chunks": chunks},
        "status_code": 200,
    }


def delete_document(doc_name: str) -> dict:
    qdrant_obj.delete_document(settings.collection_name, doc_name)
    return {
        "status": True,
        "message": f"{doc_name} deleted successfully.",
        "data": {"deleted": doc_name},
        "status_code": 200,
    }


def get_stats() -> dict:
    return {
        "status": True,
        "message": "Stats fetched successfully.",
        "data": {
            "total_chunks": qdrant_obj.count(settings.collection_name),
            "documents": qdrant_obj.list_documents(settings.collection_name),
        },
        "status_code": 200,
    }
