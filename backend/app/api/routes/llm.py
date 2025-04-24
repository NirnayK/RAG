from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db_session
from schemas.llm import LLMBase

router = APIRouter(prefix="/llm", tags=["llm"])


@router.post("/create")
async def create_llm(llm: LLMBase, session: AsyncSession = Depends(get_db_session)):
    """
    Create a new LLM.
    """
    # Logic to create a new LLM in the database
    pass


@router.get("/{llm_id}")
async def get_llm(llm_id: str, session: AsyncSession = Depends(get_db_session)):
    """
    Get LLM details by LLM ID.
    """
    # Logic to retrieve LLM details from the database
    pass


@router.put("/{llm_id}")
async def update_llm(llm_id: str, llm: LLMBase, session: AsyncSession = Depends(get_db_session)):
    """
    Update LLM details.
    """
    # Logic to update LLM details in the database
    pass


@router.delete("/{llm_id}")
async def delete_llm(llm_id: str, session: AsyncSession = Depends(get_db_session)):
    """
    Delete an LLM by LLM ID.
    """
    # Logic to delete an LLM from the database
    pass


@router.get("/list")
async def list_llms(session: AsyncSession = Depends(get_db_session)):
    """
    List all LLMs.
    """
    # Logic to retrieve all LLMs from the database
    pass
