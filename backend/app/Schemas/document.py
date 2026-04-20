from networkx import communicability_betweenness_centrality
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentResponse(BaseModel):
    id: str
    filename : str
    content_type: Optional[str] = None
    storage_path: str
    status: str
    parse_error: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

        