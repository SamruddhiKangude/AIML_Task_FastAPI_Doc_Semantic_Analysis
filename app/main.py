from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.api.routes import auth, documents, rag, roles
from app.core.config import settings
from app.db.base import Base
from app.db.init_db import seed_roles
from app.db.session import SessionLocal, engine

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_roles(db)
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(roles.router)
app.include_router(rag.router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": settings.app_name}


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    return Response(status_code=204)
