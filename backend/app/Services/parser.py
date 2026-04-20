from llama_cloud_services import LlamaParse

from app.core.config import settings

def parse_document(file_path: str) -> str:
    parser = LlamaParse(
        api_key=settings.LLAMA_CLOUD_API_KEY,
        result_type="markdown",
    )

    documents = parser.load_data(file_path)
    parsed_text = "\n\n".join([doc.text for doc in documents])
    return parsed_text