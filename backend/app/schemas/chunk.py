from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Chunk(BaseModel):
    id: UUID
    document_id: UUID
    questions: Optional[list[str]] = None
    keywords: Optional[list[str]] = None
    vector: Optional[list[float]] = None
    metadata: Optional[dict] = None
    status: Optional[bool] = True
