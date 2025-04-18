# Standard Library
import uuid
from datetime import datetime
from typing import Optional

# Third‑Party Libraries
from pydantic import BaseModel


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
