from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from api.schemas import QueryRequest
from api.views import (
    upload_file,
    query_document,
    get_documents,
    get_doc_chunks,
    delete_document,
    get_stats,
)
from core.log_config import log_message


api_router = APIRouter()


@api_router.post("/upload")
async def upload_file_route(file: UploadFile = File(...)):
    try:
        data = await upload_file(file)
        return JSONResponse(
            content={
                "status": data.get("status"),
                "message": data.get("message"),
                "data": data.get("data", None),
            },
            status_code=data.get("status_code", 200),
        )
    except Exception as e:
        log_message(
            f"Upload failed for {file.filename}: {e}", file_name="api_log", error=True
        )
        return JSONResponse(
            content={"status": False, "message": "Something went wrong.", "data": None},
            status_code=500,
        )


@api_router.post("/query")
def query_route(req: QueryRequest):
    try:
        data = query_document(req.question)
        return JSONResponse(
            content={
                "status": data.get("status"),
                "message": data.get("message"),
                "data": data.get("data", None),
            },
            status_code=data.get("status_code", 200),
        )
    except Exception as e:
        log_message(
            f"Query failed for question='{req.question}': {e}",
            file_name="api_log",
            error=True,
        )
        return JSONResponse(
            content={"status": False, "message": "Something went wrong.", "data": None},
            status_code=500,
        )


@api_router.get("/documents")
def get_documents_route():
    try:
        data = get_documents()
        return JSONResponse(
            content={
                "status": data.get("status"),
                "message": data.get("message"),
                "data": data.get("data", None),
            },
            status_code=data.get("status_code", 200),
        )
    except Exception as e:
        log_message(f"Failed to fetch documents: {e}", file_name="api_log", error=True)
        return JSONResponse(
            content={"status": False, "message": "Something went wrong.", "data": None},
            status_code=500,
        )


@api_router.get("/documents/{doc_name}/chunks")
def get_doc_chunks_route(doc_name: str):
    try:
        data = get_doc_chunks(doc_name)
        return JSONResponse(
            content={
                "status": data.get("status"),
                "message": data.get("message"),
                "data": data.get("data", None),
            },
            status_code=data.get("status_code", 200),
        )
    except Exception as e:
        log_message(
            f"Failed to fetch chunks for doc='{doc_name}': {e}",
            file_name="api_log",
            error=True,
        )
        return JSONResponse(
            content={"status": False, "message": "Something went wrong.", "data": None},
            status_code=500,
        )


@api_router.delete("/documents/{doc_name}")
def delete_document_route(doc_name: str):
    try:
        data = delete_document(doc_name)
        return JSONResponse(
            content={
                "status": data.get("status"),
                "message": data.get("message"),
                "data": data.get("data", None),
            },
            status_code=data.get("status_code", 200),
        )
    except Exception as e:
        log_message(
            f"Failed to delete doc='{doc_name}': {e}", file_name="api_log", error=True
        )
        return JSONResponse(
            content={"status": False, "message": "Something went wrong.", "data": None},
            status_code=500,
        )


@api_router.get("/stats")
def stats_route():
    try:
        data = get_stats()
        return JSONResponse(
            content={
                "status": data.get("status"),
                "message": data.get("message"),
                "data": data.get("data", None),
            },
            status_code=data.get("status_code", 200),
        )
    except Exception as e:
        log_message(f"Failed to fetch stats: {e}", file_name="api_log", error=True)
        return JSONResponse(
            content={"status": False, "message": "Something went wrong.", "data": None},
            status_code=500,
        )
