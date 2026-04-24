# Screenshot Plan (Submission Ready)

Take these screenshots from Swagger UI (`http://127.0.0.1:8000/docs`) and save with same names.

1. `01_register_success.png`

- Endpoint: `POST /auth/register`
- Show: Request body + `201 Created` response

2. `02_login_success.png`

- Endpoint: `POST /auth/login`
- Show: `access_token` and `token_type`

3. `03_roles_user.png`

- Endpoint: `GET /users/{id}/roles`
- Show: User has `Admin` and/or `Client`

4. `04_upload_success.png`

- Endpoint: `POST /documents/upload`
- Show: `document_id`, `title`, `company_name`, `document_type`

5. `05_documents_list.png`

- Endpoint: `GET /documents`
- Show: Uploaded documents list

6. `06_metadata_search.png`

- Endpoint: `GET /documents/search`
- Show: Filtered result using `title/company_name/document_type`

7. `07_rag_index_success.png`

- Endpoint: `POST /rag/index-document`
- Show: `chunks_indexed`

8. `08_rag_search_success.png`

- Endpoint: `POST /rag/search`
- Show: query + top ranked chunks with scores

9. `09_rag_context_success.png`

- Endpoint: `GET /rag/context/{document_id}`
- Show: context chunks payload

10. `10_client_403_upload.png`

- Endpoint: `POST /documents/upload` (with Client-only user)
- Show: `403 Forbidden` proof for RBAC

Optional: 11. `11_health_check.png`

- Endpoint: `GET /`
- Show: `{"status":"ok"...}`
