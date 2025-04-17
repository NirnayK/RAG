import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class KbBase(BaseModel):
    llm_model_id: str
    embedding_model_id: str
    name: str
    document_count: int
    parser: str


class KbOut(KbBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class KbCreate(KbBase):
    parser_config: dict
    is_external_bucket: bool
    bucket_config: Optional[dict] = None


class KbUpdate(BaseModel):
    llm_model_id: Optional[str] = None
    embedding_model_id: Optional[str] = None
    name: Optional[str] = None
    document_count: Optional[int] = None
    parser: Optional[str] = None
    parser_config: Optional[dict] = None
    is_external_bucket: Optional[bool] = None
    bucket_config: Optional[dict] = None
