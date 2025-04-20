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

    def mark_deleted(self, db_session: AsyncSession):
        self.deleted_at = datetime.now(timezone.utc)
        db_session.add(self)
        db_session.commit()


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

    chunk_count = Column(Integer, default=0)
    parser = Column(String(255), nullable=False, default="default")
    parser_config = Column(JSON, nullable=False)


class LLMSettings(Base, DbBaseModel):
    __tablename__ = "llm_settings"

    temperature = Column(Float, nullable=False, default=0.7)
    top_p = Column(Float, nullable=False, default=1.0)
    max_tokens = Column(Integer, nullable=False, default=150)
    frequency_penalty = Column(Float, nullable=False, default=0.0)
    presence_penalty = Column(Float, nullable=False, default=0.0)
    tools = Column(ARRAY, nullable=True)

    assistant = relationship("Assistant", back_populates="llm_settings", uselist=False)


class RetrievalSettings(Base, DbBaseModel):
    __tablename__ = "retrieval_settings"

    top_k = Column(Integer, nullable=False, default=5)
    similarity_threshold = Column(Float, nullable=False, default=0.7)
    similarity_index = Column(String(16), nullable=False, default="cosine")
    rerank_model_id = Column(UUID(as_uuid=True), ForeignKey("llms.id"), nullable=True)

    assistant = relationship("Assistant", back_populates="retrieval_settings", uselist=False)


class PromptSettings(Base, DbBaseModel):
    __tablename__ = "prompt_settings"

    system_prompt = Column(String, nullable=True, default="")
    variables = Column(ARRAY, nullable=True)

    assistant = relationship("Assistant", back_populates="prompt_settings", uselist=False)


class AssistantSettings(Base, DbBaseModel):
    __tablename__ = "assistant_settings"

    keyword_generation = Column(Boolean, nullable=False, default=False)
    empty_response = Column(String(256), nullable=False, default="")
    greeting_message = Column(String(1024), nullable=False, default="")

    assistant = relationship("Assistant", back_populates="assistant_settings", uselist=False)


class MemorySettings(Base, DbBaseModel):
    __tablename__ = "memory_settings"

    enable_user_memory = Column(Boolean, nullable=False, default=False)
    enable_conversation_memory = Column(Boolean, nullable=False, default=False)
    embedding_model_id = Column(UUID(as_uuid=True), ForeignKey("llms.id"), nullable=True)
    user_top_k = Column(Integer, nullable=False, default=5)
    conversation_top_k = Column(Integer, nullable=False, default=5)

    assistant = relationship("Assistant", back_populates="memory_settings", uselist=False)


class Assistant(Base, DbBaseModel):
    __tablename__ = "assistants"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    llm_id = Column(UUID(as_uuid=True), ForeignKey("llms.id"), nullable=False)

    knowledge_base_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=False)

    llm_settings_id = Column(UUID(as_uuid=True), ForeignKey("llm_settings.id"), nullable=False)
    retrieval_settings_id = Column(UUID(as_uuid=True), ForeignKey("retrieval_settings.id"), nullable=False)
    memory_settings_id = Column(UUID(as_uuid=True), ForeignKey("memory_settings.id"), nullable=False)
    prompt_settings_id = Column(UUID(as_uuid=True), ForeignKey("prompt_settings.id"), nullable=False)
    assistant_settings_id = Column(UUID(as_uuid=True), ForeignKey("assistant_settings.id"), nullable=False)

    llm_settings = relationship("LLMSettings", back_populates="assistant")
    retrieval_settings = relationship("RetrievalSettings", back_populates="assistant")
    memory_settings = relationship("MemorySettings", back_populates="assistant")
    prompt_settings = relationship("PromptSettings", back_populates="assistant")
    assistant_settings = relationship("AssistantSettings", back_populates="assistant")
