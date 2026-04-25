import time
import traceback
from app.services.cleaner import clean_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_texts
from app.services.vector_store import get_client, CLASS_NAME
from app.db.models import Document
from app.db.chunk_model import DocumentChunk
from app.db.session import SessionLocal
from app.services.parser import parse_document

def process_document(document_id: str):
    """Full pipeline: parse -> clean -> chunk -> embed -> store in Weaviate."""
    db = SessionLocal()
    client = None

    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            print(f"[ERROR] Document not found: {document_id}")
            return

        print(f"[PROCESS] Starting processing for: {doc.filename} (id={document_id})")

        # Step 1: Parse
        doc.status = "PROCESSING"
        db.commit()

        parsed_text = parse_document(doc.storage_path)
        if not parsed_text or not parsed_text.strip():
            doc.status = "FAILED"
            doc.parse_error = "Parser returned empty text"
            db.commit()
            print(f"[ERROR] Parser returned empty text for {doc.filename}")
            return

        doc.parsed_text = parsed_text
        doc.status = "PARSED"
        doc.parse_error = None
        db.commit()
        print(f"[PROCESS] Parsed successfully: {len(parsed_text)} chars")

        # Step 2: Clean + Chunk
        cleaned = clean_text(parsed_text)
        chunks = chunk_text(cleaned)

        if not chunks:
            doc.status = "FAILED"
            doc.parse_error = "No chunks produced from parsed text"
            db.commit()
            print(f"[ERROR] No chunks produced for {doc.filename}")
            return

        print(f"[PROCESS] Chunks created: {len(chunks)}")

        # Step 3: Embed with rate-limit throttling
        texts = [c["content"] for c in chunks]
        embeddings = []
        for i, text in enumerate(texts):
            vec = embed_texts([text])[0]
            embeddings.append(vec)
            # Throttle to avoid Gemini free-tier 15 RPM rate limit
            if i < len(texts) - 1:
                time.sleep(4.5)
            if (i + 1) % 5 == 0:
                print(f"[PROCESS] Embedded {i+1}/{len(texts)} chunks...")

        print(f"[PROCESS] Embeddings created: {len(embeddings)}")

        # Step 4: Store in Weaviate + Postgres
        client = get_client()
        collection = client.collections.get(CLASS_NAME)

        for chunk, vector in zip(chunks, embeddings):
            db_chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=chunk["chunk_index"],
                content=chunk["content"],
                token_count=chunk["token_count"],
            )
            db.add(db_chunk)

            collection.data.insert(
                properties={
                    "document_id": document_id,
                    "content": chunk["content"],
                    "chunk_index": chunk["chunk_index"],
                    "token_count": chunk["token_count"],
                },
                vector=vector,
            )

        doc.status = "INDEXED"
        db.commit()
        print(f"[SUCCESS] Document indexed: {doc.filename} ({document_id})")

    except Exception as e:
        print(f"[ERROR] Indexing failed for {document_id}: {e}")
        traceback.print_exc()
        try:
            doc = db.query(Document).filter(Document.id == document_id).first()
            if doc:
                doc.status = "FAILED"
                doc.parse_error = str(e)[:500]
                db.commit()
        except Exception:
            pass

    finally:
        if client:
            try:
                client.close()
            except Exception:
                pass
        db.close()