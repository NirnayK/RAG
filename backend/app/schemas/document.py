from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class DocumentBase(BaseModel):
    knowledge_base_id: str
    name: str


class DocumentUpdate(DocumentBase):
    location_config: Optional[dict] = None
    parser_config: Optional[dict] = None
    parser: Optional[str] = None
    redo_chunks: Optional[bool] = True


class DocumentOut(DocumentBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
