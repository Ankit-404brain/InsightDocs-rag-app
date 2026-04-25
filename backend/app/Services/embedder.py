from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def embed_texts(texts: list[str]) -> list[list[float]]:
    vectors: list[list[float]] = []
    for text in texts:
        result = client.models.embed_content(
            model=settings.GEMINI_EMBED_MODEL,
            contents=text,
        )
        vectors.append(result.embeddings[0].values)
    return vectors