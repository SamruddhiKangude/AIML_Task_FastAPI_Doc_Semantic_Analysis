# FastAPI Financial Document Management with Semantic Analysis

This project provides a production-style FastAPI backend for financial document management with role-based access control and semantic retrieval.

## Quick Start (Steps of How run Project)

1. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
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

Wait For Few Min aprox (2min)

```INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [14460] using WatchFiles
INFO:     Started server process [15280]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:49817 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:49817 - "GET /openapi.json HTTP/1.1" 200 OK
```

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

### How to change a user's role (after running the program)

Use one of these two methods — the API (recommended) or direct DB SQL. Replace `ADMIN_BEARER_TOKEN` with a valid Admin JWT.

- API (curl) — assign role to `user_id = 3`:

```bash
curl -X POST "http://localhost:8000/users/assign-role" \
  -H "Authorization: Bearer ADMIN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 3, "role_name": "Admin"}'
```

- Direct DB (SQL) — remove existing roles and set `Admin` for `user_id = 3`:

```sql
-- (optional) inspect roles
SELECT id, name FROM roles;

-- remove all roles for user 3
DELETE FROM user_roles WHERE user_id = 3;

-- add Admin role for user 3
INSERT INTO user_roles (user_id, role_id)
VALUES (3, (SELECT id FROM roles WHERE name = 'Admin'));
```

Or to only remove the `Client` role and add `Admin`:

```sql
DELETE FROM user_roles
WHERE user_id = 3
  AND role_id = (SELECT id FROM roles WHERE name = 'Client');

INSERT INTO user_roles (user_id, role_id)
VALUES (3, (SELECT id FROM roles WHERE name = 'Admin'));
```

### RAG

- `POST /rag/index-document`
- `DELETE /rag/remove-document/{id}`
- `POST /rag/search`
- `GET /rag/context/{document_id}`

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
