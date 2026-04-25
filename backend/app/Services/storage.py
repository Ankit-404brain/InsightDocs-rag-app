import os
import tempfile
from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile

# Use system temp directory to avoid triggering fastapi dev auto-reload
UPLOAD_DIR = Path(tempfile.gettempdir()) / "insightdocs_uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_upload_file_sync(file: UploadFile) -> str:
    """Save uploaded file synchronously and return the absolute path."""
    extension = Path(file.filename).suffix
    unique_name = f"{uuid4()}{extension}"
    destination = UPLOAD_DIR / unique_name

    content = file.file.read()
    destination.write_bytes(content)

    return str(destination)