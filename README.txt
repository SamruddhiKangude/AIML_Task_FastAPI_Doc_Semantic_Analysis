FastAPI Financial Document Management with Semantic Analysis

Project Summary
This project is a FastAPI backend for financial document management with:
- JWT authentication
- Role-based access control (RBAC)
- Financial document upload and metadata search
- RAG (Retrieval-Augmented Generation) indexing and semantic search using embeddings + reranking

Tech Stack
- FastAPI
- SQLAlchemy + SQLite
- JWT (python-jose)
- Passlib (password hashing)
- LangChain text splitters
- SentenceTransformers (embeddings + reranker)
- Qdrant client (auto-fallback to embedded mode if remote Qdrant is unavailable)


============================================================
LINE-BY-LINE EXECUTION (WINDOWS POWERSHELL)
============================================================

1) Open PowerShell in project folder
Command:
cd D:\AIML

2) Create virtual environment
Command:
python -m venv .venv

3) Activate virtual environment
Command:
.\.venv\Scripts\Activate.ps1

If activation is blocked, run this first, then activate again:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1

4) Install dependencies
Command:
pip install -r requirements.txt

5) Create environment file
Command:
Copy-Item .env.example .env

6) Run the API server
Command:
uvicorn app.main:app --reload

7) Open API docs in browser
URL:
http://127.0.0.1:8000/docs


============================================================
COMPLETE API TEST FLOW (STEP-BY-STEP)
============================================================

Step 1: Register a user
Endpoint:
POST /auth/register
Sample body:
{
  "email": "soham@gmail.com",
  "full_name": "Soham Santosh Pawar",
  "password": "Soham@1234",
  "company_name": "abc"
}
Expected result:
201 Created

Step 2: Login
Endpoint:
POST /auth/login
Form fields:
- grant_type: password
- username: soham@gmail.com
- password: Soham@1234
- scope: (keep empty)
- client_id: (keep empty)
- client_secret: (keep empty)
Expected result:
200 OK with access_token

Step 3: Authorize in Swagger
Action:
- Click Authorize button
- Enter username and password in OAuth2 form
- Click Authorize

Step 4: Check current roles
Endpoint:
GET /users/1/roles
Expected initial role:
Client

Step 5: Assign Admin role (one-time setup for full testing)
Run this PowerShell command in D:\AIML:
python -c "import sqlite3; c=sqlite3.connect('finance_docs.db'); cur=c.cursor(); cur.execute('select id from users where email=?',('soham@gmail.com',)); u=cur.fetchone()[0]; cur.execute('select id from roles where name=?',('Admin',)); r=cur.fetchone()[0]; cur.execute('insert or ignore into user_roles(user_id, role_id) values(?,?)',(u,r)); c.commit(); c.close(); print('Admin role assigned')"

Step 6: Login again and re-authorize
Reason:
Role changes should be reflected in new token/session.

Step 7: Upload document
Endpoint:
POST /documents/upload
Form-data fields:
- title: Q1 Financial Report
- company_name: abc
- document_type: report
- file: choose .txt / .pdf / .docx
Expected result:
201 Created with document_id

Step 8: List documents
Endpoint:
GET /documents
Expected result:
List containing uploaded document metadata

Step 9: Metadata search
Endpoint:
GET /documents/search
Try filters using query params:
- title=Q1
- company_name=abc
- document_type=report
Expected result:
Filtered document list

Step 10: Index document in vector database
Endpoint:
POST /rag/index-document
Sample body:
{
  "document_id": 1
}
Use your actual uploaded document_id.
Expected result:
"chunks_indexed" should be greater than 0

Step 11: Semantic search
Endpoint:
POST /rag/search
Sample body:
{
  "query": "high debt ratio risk",
  "limit": 5
}
Expected result:
Top semantically relevant chunks with scores and rerank_score

Step 12: Get document context chunks
Endpoint:
GET /rag/context/1
Use your actual document_id.
Expected result:
Chunked context payload for the document


============================================================
PERMISSION TEST (RBAC VALIDATION)
============================================================

Goal:
Verify that Client role cannot upload documents.

Procedure:
1) Register a new user (do not assign Admin role)
2) Login as that user
3) Call POST /documents/upload
Expected result:
403 Forbidden


============================================================
IMPORTANT NOTES
============================================================

1) GET /auth/register returns 405 by design
- Register endpoint supports POST only.

2) If remote Qdrant is not running
- App automatically falls back to embedded local Qdrant.
- No manual Qdrant setup is required for local testing.

3) Supported upload formats in current code
- .txt
- .pdf
- .docx

4) Security note
- Keep SECRET_KEY private in .env
- Do not commit .env to GitHub


============================================================
SUBMISSION CHECKLIST
============================================================

Include these in your final submission:
1) Swagger screenshot for successful register
2) Swagger screenshot for successful document upload
3) Swagger screenshot for successful /rag/search
4) Swagger screenshot for 403 Forbidden on Client upload test
5) 1-2 JSON sample responses (register, upload, rag/search)
6) This README.txt file


Project Status
All required modules are implemented and tested:
- Authentication and JWT
- RBAC and permissions
- Document upload and metadata retrieval/search
- RAG indexing and semantic search with reranking

Submission Artifacts
- submission/SUBMISSION_CHECKLIST.md
- submission/SCREENSHOT_LIST.md
- submission/SAMPLE_RESPONSES.json
