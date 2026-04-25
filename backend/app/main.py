from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.api.routes.documents import router as documents_router
from app.api.routes.chat import router as chat_router
from app.services.vector_store import create_schema


app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Initialize databases
Base.metadata.create_all(bind=engine)

try:
    create_schema()
except Exception as e:
    print(f"[WARNING] Could not initialize Weaviate schema: {e}")

app.include_router(documents_router, prefix="/api/documents", tags=["documents"])

app.include_router(chat_router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {
       "message": f"{settings.APP_NAME} is running",
       "environment": settings.APP_ENV
    }

@app.get("/health")
def health():
    return {"status": "ok"}