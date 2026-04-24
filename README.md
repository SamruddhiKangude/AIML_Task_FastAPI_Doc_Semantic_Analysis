# FastAPI Financial Document Management with Semantic Analysis

This project provides a production-style FastAPI backend for financial document management with role-based access control and semantic retrieval.

## Features

- JWT Authentication (`/auth/register`, `/auth/login`)
- RBAC for `Admin`, `Financial Analyst`, `Auditor`, `Client`
- Financial document upload and metadata retrieval
- Metadata search for documents
- RAG pipeline:
  - document text extraction
  - semantic chunking with LangChain splitter
  - embedding generation with SentenceTransformers
  - vector storage in Qdrant
  - semantic retrieval + reranking

## Metadata Fields

- `document_id`
- `title`
- `company_name`
- `document_type` (`invoice`, `report`, `contract`)
- `uploaded_by`
- `created_at`

## API Endpoints

### Authentication

- `POST /auth/register`
- `POST /auth/login`

### Documents

- `POST /documents/upload`
- `GET /documents`
- `GET /documents/{document_id}`
- `DELETE /documents/{document_id}`
- `GET /documents/search`

### Roles and Permissions

- `POST /roles/create`
- `POST /users/assign-role`
- `GET /users/{id}/roles`
- `GET /users/{id}/permissions`

### RAG

- `POST /rag/index-document`
- `DELETE /rag/remove-document/{id}`
- `POST /rag/search`
- `GET /rag/context/{document_id}`

## Quick Start

1. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Copy env config

```powershell
Copy-Item .env.example .env
```

4. Run API

```powershell
uvicorn app.main:app --reload
```

5. Open docs

- http://127.0.0.1:8000/docs

## RAG Retrieval Pipeline

1. Upload document using `/documents/upload`
2. Generate embeddings with `/rag/index-document`
3. Search by meaning with `/rag/search`
4. Retrieve indexed context chunks with `/rag/context/{document_id}`

## Example Semantic Search Request

```json
{
  "query": "financial risk related to high debt ratio",
  "limit": 5
}
```

## Notes

- If Qdrant server is unavailable, the service falls back to in-memory Qdrant for local development.
- To enforce strict multi-tenant access for clients, set each client's `company_name` at registration.
