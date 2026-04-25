from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.embedder import embed_texts
from app.services.vector_store import get_client, CLASS_NAME
from app.services.llm import generate_answer

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
def query_rag(request: QueryRequest):
    query = request.query

    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    client = get_client()

    try:
        # Embed the query
        query_vector = embed_texts([query])[0]

        # Search Weaviate
        collection = client.collections.get(CLASS_NAME)

        response = collection.query.near_vector(
            near_vector=query_vector,
            limit=5,
            return_properties=["content", "document_id", "chunk_index"],
        )

        chunks = []
        for obj in response.objects:
            chunks.append({
                "content": obj.properties.get("content", ""),
                "document_id": obj.properties.get("document_id", ""),
                "chunk_index": obj.properties.get("chunk_index", 0),
            })

        if not chunks:
            return {"answer": "No relevant documents found. Please upload and index documents first.", "sources": []}

        # Build context and generate answer
        context = "\n\n---\n\n".join(
            [f"[Chunk {c['chunk_index']} from doc {c['document_id']}]\n{c['content']}" for c in chunks]
        )

        answer = generate_answer(query, context)

        return {
            "answer": answer,
            "sources": chunks,
        }

    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

    finally:
        client.close()