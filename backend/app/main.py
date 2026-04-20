from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.api.routes.documents import router as documents_router


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

Base.metadata.create_all(bind=engine)

app.include_router(documents_router, prefix="/api/documents", tags=["documents"])

@app.get("/")
def read_root():
    return {
       "message": f"{settings.APP_NAME} is running",
       "environment": settings.APP_ENV
    }

@app.get("/health")
def health():
    return {"status": "ok"}