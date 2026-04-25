from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_answer(query: str, context: str) -> str:
    prompt = f"""You are a grounded RAG assistant.
Answer only from the context provided below.
If the answer is not in the context, say "I don't have enough information to answer that."
Cite the chunk labels (e.g., [Chunk 0], [Chunk 1]) in your answer when relevant.

Context:
{context}

Question:
{query}

Answer:"""

    response = client.models.generate_content(
        model=settings.GEMINI_CHAT_MODEL,
        contents=prompt,
    )
    return response.text or "No response generated."