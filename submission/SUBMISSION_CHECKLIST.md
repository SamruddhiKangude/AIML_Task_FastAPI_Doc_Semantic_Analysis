# Final Submission Checklist

## 1. Project Files

- [ ] Source code folder included (`app/`)
- [ ] Dependency file included (`requirements.txt`)
- [ ] Environment sample included (`.env.example`)
- [ ] Final execution guide included (`README.txt`)

## 2. Mandatory API Coverage Proof

- [ ] `POST /auth/register` success
- [ ] `POST /auth/login` success
- [ ] `POST /documents/upload` success
- [ ] `GET /documents` success
- [ ] `GET /documents/{document_id}` success
- [ ] `DELETE /documents/{document_id}` tested (optional screenshot if required)
- [ ] `GET /documents/search` success
- [ ] `POST /roles/create` tested
- [ ] `POST /users/assign-role` tested
- [ ] `GET /users/{id}/roles` success
- [ ] `GET /users/{id}/permissions` success
- [ ] `POST /rag/index-document` success
- [ ] `DELETE /rag/remove-document/{id}` tested (optional screenshot if required)
- [ ] `POST /rag/search` success
- [ ] `GET /rag/context/{document_id}` success

## 3. RBAC Validation

- [ ] Admin can upload documents
- [ ] Client cannot upload documents (403 expected)
- [ ] Client can view only allowed company documents

## 4. RAG Validation

- [ ] Document chunking and indexing done
- [ ] Semantic search returns ranked chunks
- [ ] Context retrieval returns document chunk payload

## 5. Attachments Required

- [ ] Screenshots listed in `SCREENSHOT_LIST.md`
- [ ] Sample JSON responses from `SAMPLE_RESPONSES.json`

## 6. Final Reviewer Notes

- [ ] Mention: JWT used for auth
- [ ] Mention: Role-based authorization implemented
- [ ] Mention: Vector DB + reranking pipeline implemented
- [ ] Mention: Qdrant fallback for local development

## 7. Final Packaging

- [ ] Zip project folder (exclude `.venv/`)
- [ ] Confirm app runs with commands in `README.txt`
- [ ] Verify all links/files open before submission
