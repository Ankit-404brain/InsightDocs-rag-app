from fastapi import APIRouter, Depends, UploadFile, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Document
from app.schemas.document import DocumentResponse
from app.services.storage import save_upload_file_sync
from app.workers.tasks import process_document

router = APIRouter()

ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).order_by(Document.created_at.desc()).all()
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.post("/upload")
def upload_document(file: UploadFile, background_tasks: BackgroundTasks):
    db = SessionLocal()

    try:
        # Save file to temp directory (outside project dir to avoid auto-reload)
        file_path = save_upload_file_sync(file)

        doc = Document(
            filename=file.filename,
            storage_path=file_path,
            status="UPLOADED"
        )

        db.add(doc)
        db.commit()
        db.refresh(doc)

        doc_id = str(doc.id)
    finally:
        db.close()

    # Queue background processing
    background_tasks.add_task(process_document, doc_id)

    return {"id": doc_id, "status": "UPLOADED"}