import uuid
from datetime import datetime, timezone

from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, Integer,
                        SmallInteger, String, ARRAY)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)


class User(Base, BaseModel):
    __tablename__ = "users"

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)


class LLMs(Base, BaseModel):
    __tablename__ = "llms"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    provider = Column(String(255), nullable=False, index=True)
    model_name = Column(String(255), nullable=False)
    api_base = Column(String(255), nullable=True)


class KnowledgeBase(Base, BaseModel):
    __tablename__ = "knowledge_bases"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    llm_model_id = Column(UUID(as_uuid=True), ForeignKey("llms.id"), nullable=False)
    embedding_model_id = Column(UUID(as_uuid=True), ForeignKey("llms.id"), nullable=False)

    name = Column(String(255), nullable=False)
    document_count = Column(Integer, default=0)
    parser = Column(String(255), nullable=False, default="general")
    parser_config = Column(JSON, nullable=False)

    is_external_bucket = Column(Boolean, nullable=False, default=False)
    bucket_config = Column(JSON, nullable=True)


class Document(Base, BaseModel):
    __tablename__ = "documents"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    knowledge_base_id = Column(UUID(as_uuid=True), ForeignKey("knowledgebases.id"), nullable=False)

    name = Column(String(255), nullable=False)
    status = Column(String(64), nullable=False, default="pending")
    progress = Column(SmallInteger, nullable=False, default=0)
    location = Column(String(4096), nullable=False)

    chunk_count = Column(Integer, default=0)
    parser = Column(String(255), nullable=False, default="default")
    parser_config = Column(JSON, nullable=False)


class Assistant(Base, BaseModel):
    __tablename__ = "assistants"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    knowledge_bases = Column(ARRAY, nullable=False)

    name = Column(String(255), nullable=False)

    llm_id = Column(UUID(as_uuid=True), ForeignKey("llms.id"), nullable=False)
    llm_settings = Column(JSON, nullable=False)
    retrieval_settings = Column(JSON, nullable=False)
    memory_settings = Column(JSON, nullable=False)
    prompt_settings = Column(JSON, nullable=False)
    assistant_settings = Column(JSON, nullable=False)
