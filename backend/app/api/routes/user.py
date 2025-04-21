from fastapi import APIRouter, Depends, Request
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from constants.common import SAVE, UPDATE
from core.db import get_db
from core.security import get_current_user_id
from models import User
from schemas.user import UserCreate, UserOut, UserUpdate
from services.response import BaseResponse
from validators.user import UserValidator

router = APIRouter(prefix="/user", tags=["user"])
resp = BaseResponse(model=UserOut)


@router.post("/create")
async def create_user(user: UserCreate, request: Request, db: AsyncSession = Depends(get_db)):
    """
    Create a new user.
    """
    # Validate user data
    validator = UserValidator(db=db, data=user)

    if not await validator.is_valid(SAVE):
        logger.error("Validation failed for create user: {}", validator.errors)
        return resp.bad_request(errors=validator.errors, message="Validation failed")

    # Save user to database
    db_user = await validator.save()
    logger.info("User created successfully - id: {}", db_user.id)
    return resp.created(data=db_user, message="User created successfully")


@router.get("/me")
async def get_user(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Get user details by user ID.
    """
    logger.info("GET /user/me - user_id: {}", user_id)
    query = select(User).filter(User.id == user_id, User.deleted_at.is_(None))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        logger.warning("User not found - id: {}", user_id)
        return resp.not_found(message="User not found")

    logger.info("User retrieved successfully - id: {}", user_id)
    return resp.ok(data=user)


@router.put("/me")
async def update_user(
    user: UserUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Update user details.
    """
    logger.info("PUT /user/me - user_id: {}, payload: {}", user_id, user.model_dump())
    query = select(User).filter(User.id == user_id, User.deleted_at.is_(None))
    result = await db.execute(query)
    db_user = result.scalar_one_or_none()

    if not db_user:
        logger.warning("User not found for update - id: {}", user_id)
        return resp.not_found(message="User not found")

    # Validate and update user
    validator = UserValidator(db=db, data=user)

    if not await validator.is_valid(UPDATE):
        logger.error("Validation failed for update user: {}", validator.errors)
        return resp.bad_request(errors=validator.errors, message="Validation failed")

    # Update user
    updated_user = await validator.update(db_user)
    logger.info("User updated successfully - id: {}", user_id)
    return resp.ok(data=updated_user, message="User updated successfully")


@router.delete("/me")
async def delete_user(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a user by user ID (soft delete).
    """
    logger.info("DELETE /user/me - user_id: {}", user_id)
    query = select(User).filter(User.id == user_id, User.deleted_at.is_(None))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        logger.warning("User not found for delete - id: {}", user_id)
        return resp.not_found(message="User not found")

    await user.mark_deleted(db)
    logger.info("User deleted successfully - id: {}", user_id)
    return resp.ok(message="User deleted successfully")
