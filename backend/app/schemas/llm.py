from typing import Optional

from pydantic import BaseModel


class LLMBase(BaseModel):
    provider: str
    model_name: str
    api_base: Optional[str] = None
    api_key: str


class LLMOut(LLMBase):
    pass
