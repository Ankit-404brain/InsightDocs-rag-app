import tiktoken

CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

encoding = tiktoken.get_encoding("cl100k_base")

def chunk_text(text: str):
    tokens = encoding.encode(text)

    chunks = []
    start = 0
    idx = 0

    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk_tokens = tokens[start:end]

        chunk_text = encoding.decode(chunk_tokens)

        chunks.append({
            "chunk_index": idx,
            "content": chunk_text,
            "token_count": len(chunk_tokens)
        })

        start += CHUNK_SIZE - CHUNK_OVERLAP
        idx += 1

    return chunks