# Doc Intel

A local RAG (Retrieval-Augmented Generation) application that lets you upload documents, index them, and ask questions - with exact page citations. Runs entirely on your machine with no external API calls.

**Stack:** FastAPI · Ollama · Qdrant · Tesseract OCR

---

## Supported Formats

PDF · DOCX · PPTX · XLSX · CSV · TXT · MD · JPG · PNG · WEBP · BMP · TIFF · SVG

---

## Prerequisites

### 1. Docker (for Qdrant)

Install Docker Desktop from https://www.docker.com/products/docker-desktop and make sure it's running.

### 2. Ollama

Install Ollama from https://ollama.com/download, then pull the required models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

Ollama runs as a background service automatically after installation and listens on `http://localhost:11434`.

### 3. Tesseract OCR

Required for OCR on scanned PDFs and images.

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt install tesseract-ocr
```

**Windows:**  
Download the installer from https://github.com/UB-Mannheim/tesseract/wiki and add it to your PATH.

### 4. Python 3.11+

```bash
python3 --version  # should be 3.11 or higher
```

---

## Setup & Running

### 1. Start Qdrant

```bash
docker compose up -d
```

This starts Qdrant in the background on port `6333`. Data is persisted in a Docker volume so it survives restarts.

### 2. Create virtualenv and install dependencies

```bash
python3 -m venv env
source env/bin/activate        # Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Start the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open http://localhost:8000 in your browser.

---

## Configuration

All settings can be overridden via a `.env` file in the project root:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `EMBED_MODEL` | `nomic-embed-text` | Embedding model |
| `LLM_MODEL` | `llama3.2` | Chat/query model |
| `QDRANT_HOST` | `localhost` | Qdrant host |
| `QDRANT_PORT` | `6333` | Qdrant port |
| `COLLECTION_NAME` | `doc_intel` | Qdrant collection name |
| `CHUNK_SIZE` | `500` | Text chunk size (tokens) |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `TOP_K` | `5` | Number of chunks retrieved per query |

Example `.env`:
```env
LLM_MODEL=llama3.1:8b
EMBED_MODEL=nomic-embed-text
TOP_K=8
```

---

## Stopping

```bash
# Stop the server: Ctrl+C

# Stop Qdrant
docker compose down
```
