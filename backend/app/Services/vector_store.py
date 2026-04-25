import weaviate
from weaviate.classes.config import Configure, DataType, Property

CLASS_NAME = "DocumentChunk"


def get_client():
    """Create and return a new connected Weaviate client."""
    client = weaviate.connect_to_local()
    return client


def create_schema():
    """Create the DocumentChunk collection if it doesn't exist."""
    client = get_client()
    try:
        if client.collections.exists(CLASS_NAME):
            print(f"[WEAVIATE] Collection '{CLASS_NAME}' already exists")
            return

        client.collections.create(
            name=CLASS_NAME,
            properties=[
                Property(name="document_id", data_type=DataType.TEXT),
                Property(name="content", data_type=DataType.TEXT),
                Property(name="chunk_index", data_type=DataType.INT),
                Property(name="token_count", data_type=DataType.INT),
            ],
        )
        print(f"[WEAVIATE] Created collection: {CLASS_NAME}")
    finally:
        client.close()