import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    ARRAY,
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DbBaseModel:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    deleted_at = Column(DateTime, nullable=True)


class User(Base, DbBaseModel):
    __tablename__ = "users"

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(128), nullable=False)


class LLMs(Base, DbBaseModel):
    __tablename__ = "llms"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    provider = Column(String(255), nullable=False, index=True)
    model_name = Column(String(255), nullable=False)
    api_base = Column(String(255), nullable=True)


class ParserConfig(Base, DbBaseModel):
    __tablename__ = "parser_configs"


class KnowledgeBase(Base, DbBaseModel):
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


class Document(Base, DbBaseModel):
    __tablename__ = "documents"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    knowledge_base_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id"), nullable=False)

    name = Column(String(255), nullable=False)
    status = Column(String(32), nullable=False, default="pending")
    progress = Column(SmallInteger, nullable=False, default=0)
    location = Column(String(4096), nullable=False)
    size = Column(Integer, nullable=False)

    chunk_count = Column(Integer, default=0)
    parser = Column(String(255), nullable=False, default="default")
    parser_config = Column(JSON, nullable=False)


class Assistant(Base, DbBaseModel):
    __tablename__ = "assistants"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    llm_id = Column(UUID(as_uuid=True), ForeignKey("llms.id"), nullable=False)

    knowledge_base_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=False)

    llm_settings_id = Column(JSON, nullable=False)
    retrieval_settings_id = Column(JSON, nullable=False)
    memory_settings_id = Column(JSON, nullable=False)
    prompt_settings_id = Column(JSON, nullable=False)
    assistant_settings_id = Column(JSON, nullable=False)
