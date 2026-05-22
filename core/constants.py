IMAGE_UPSCALE_MIN_WIDTH = 1000
OCR_DPI = 200
DOCX_LINES_PER_PAGE = 40
TEXT_LINES_PER_PAGE = 100
RAG_MIN_SCORE = 0.4

RAG_SYSTEM_PROMPT = """You are a document intelligence assistant.
Answer the user's question using ONLY the provided context chunks.
Be concise and factual. If the context does not contain enough information, say so clearly.
Do not make up information that is not in the context."""


RASTER_IMAGE_FORMATS = {"jpg", "jpeg", "png", "webp", "bmp", "tiff", "tif"}

SUPPORTED_FORMATS = {
    "pdf",
    "docx",
    "txt",
    "md",
    "xlsx",
    "csv",
    "pptx",
    "jpg",
    "jpeg",
    "png",
    "webp",
    "bmp",
    "tiff",
    "tif",
    "svg",
}
