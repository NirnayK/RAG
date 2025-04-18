# Standard Library
from datetime import datetime
from typing import List, Optional
from uuid import UUID

# Third‑Party Libraries
from pydantic import BaseModel


class AssistantBase(BaseModel):
    name: str
    llm_id: UUID
    knowledge_base_ids: List[UUID]


class AssistantOut(AssistantBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    llm_settings: "LLMSettings"
    retrieval_settings: "RetrievalSettings"
    memory_settings: "MemorySettings"
    prompt_settings: "PromptSettings"
    assistant_settings: "AssistantSettings"


class LLMSettings(BaseModel):
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    max_tokens: Optional[int] = 150
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0
    stop: Optional[list] = None
    tools: Optional[list] = None


class RetrievalSettings(BaseModel):
    top_k: Optional[int] = 5
    similarity_threshold: Optional[float] = 0.7
    similarity_index: Optional[str] = "cosine"
    rerank_model_id: Optional[int] = None


class PromptSettings(BaseModel):
    system_prompt: Optional[str] = ""
    variables: Optional[list] = None


class AssistantSettings(BaseModel):
    keyword_generation: Optional[bool] = False
    empty_response: Optional[str] = ""
    greeting_message: Optional[str] = ""


class MemorySettings(BaseModel):
    enable_user_memory: Optional[bool] = False  # Redis
    enable_conversation_memory: Optional[bool] = False  # Qdrant/Faiss
    embedding_model_id: Optional[str] = None
    user_top_k: Optional[int] = 5
    conversation_top_k: Optional[int] = 5


class AssistantCreate(AssistantBase):
    llm_settings: LLMSettings
    retrieval_settings: RetrievalSettings
    prompt_settings: PromptSettings
    assistant_settings: AssistantSettings
    memory_settings: MemorySettings


class AssistantUpdate(BaseModel):
    name: Optional[str] = None
    llm_id: Optional[UUID] = None
    knowledge_base_ids: Optional[List[UUID]] = None
    llm_settings: Optional[LLMSettings] = None
    retrieval_settings: Optional[RetrievalSettings] = None
    prompt_settings: Optional[PromptSettings] = None
    assistant_settings: Optional[AssistantSettings] = None
    memory_settings: Optional[MemorySettings] = None
    assistant_settings: Optional[AssistantSettings] = None
    memory_settings: Optional[MemorySettings] = None
