# FastAPI Financial Document Management with Semantic Analysis

This project provides a production-style FastAPI backend for financial document management with role-based access control and semantic retrieval.
## Quick Start (Steps to Run the Project)

### Option A - VS Code terminal (PowerShell)

Navigate to the project directory using the following commands:

```powershell
ls
```
(after running ls command you see file name like as AIML_Task_FastAPI_Doc_Semantic_Analysis-main below Length Name ....copy this and paste after cd)
```powershell
cd AIML_Task_FastAPI_Doc_Semantic_Analysis
```
Or
```powershell
cd AIML_Task_FastAPI_Doc_Semantic_Analysis-main
```
```powershell
ls
```
(if you see app, submission, .env.submission, .gitignore, finance_docs.db, README.md, README.txt, requirements.txt below Length Name Then it is ok current directory)
```

Check Prerequisites
```powershell
python --version
pip --version
git --version
```

1. Create and activate virtual environment

```powershell
python -m venv .venv
```

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

```powershell
\.venv\Scripts\Activate.ps1
```


2. Install dependencies

```powershell
pip install -r requirements.txt # ( If you get error not downloadning then open CMD and open as administrator and type command following)
```

3. Copy env config

```powershell
Copy-Item .env.example .env
```

4. Run API

```powershell
uvicorn app.main:app --reload
```

Wait untill INFO: Application Startup complete. (Then open following link in new browser)

5. Open docs

- http://127.0.0.1:8000 (firstly you see this after that in url /docs type after 8000)
  
- http://127.0.0.1:8000/docs

### Option B - Command Prompt (CMD)

Go in proper project cmd and type following commands 

1. Create and activate virtual environment

```cmd
python -m venv .venv
\.venv\Scripts\Activate
```

2. Install dependencies

```cmd
pip install -r requirements.txt
```

3. Copy env config

```cmd
copy .env.example .env
```

4. Run API

```cmd
uvicorn app.main:app --reload
```

5. Open docs

- http://127.0.0.1:8000/docs

  Wait For few min (aprox 2min)

```cmd
INFO:     Started server process [11056]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:64817 - "POST /users/assign-role HTTP/1.1" 200 OK
INFO:     127.0.0.1:57309 - "GET /users/3/permissions HTTP/1.1" 200 OK
  
  ```
6. Alternatively, you can run a Python one-liner to assign the `Admin` role by user email (replace the email as needed):

```bash
python -c "import sqlite3; c=sqlite3.connect('finance_docs.db'); cur=c.cursor(); cur.execute('select id from users where email=?',('your Email id ',)); u=cur.fetchone()[0]; cur.execute('select id from roles where name=?',('Admin',)); r=cur.fetchone()[0]; cur.execute('insert or ignore into user_roles(user_id, role_id) values(?,?)',(u,r)); c.commit(); c.close(); print('Admin role assigned')"
```

### Windows long path support (only if pip install fails)

If you see a long path error while installing (common with `torch`), enable Windows long paths:

```cmd
reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
```

Restart the PC, then run the install step again.
  
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

