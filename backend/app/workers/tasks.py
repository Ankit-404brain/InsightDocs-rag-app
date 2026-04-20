from app.db.session import SessionLocal
from app.db.models import Document
from app.Services.parser import parse_document

def process_document(document_id: str):
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return

        document.status = "PARSING"
        db.commit()

        parsed_text = parse_document(document.storage_path)

        document.parsed_text = parsed_text
        document.status = "PARSED"
        document.parse_error = None
        db.commit()

    except Exception as e:
        document = db.query(Document).filter(Document.id == document_id).first()
        if document:
            document.status = "FAILED"
            document.parse_error = str(e)
            db.commit()
    finally:
        db.close()