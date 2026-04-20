from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def save_upload_file(file: UploadFile) -> str:
    extension = Path(file.filename).suffix
    unique_name = f"{uuid4()}{extension}"
    destination = UPLOAD_DIR / unique_name

    content = await file.read()
    destination.write_bytes(content)

    return str(destination)