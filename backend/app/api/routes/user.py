from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from constants.common import SAVE, UPDATE
from core.db import get_db_session
from core.security import get_current_user_id
from models import User
from schemas.user import UserCreate, UserOut, UserUpdate
from services.common import CommonService
from services.response import BaseResponse
from validators.user import UserValidator

router = APIRouter(prefix="/user", tags=["user"])
resp = BaseResponse(model=UserOut)
db_service = CommonService(model=User)


@router.post("/create")
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_db_session)):
    """
    Create a new user.
    """
    # Validate user data
    validator = UserValidator(session=session, data=user)

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
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get user details by user ID.
    """
    logger.info("GET /user/me - user_id: {}", user_id)
    user = await db_service.get_by_id(session=session, id=user_id)

    if not user:
        logger.warning("User not found - id: {}", user_id)
        return resp.not_found(message="User not found")

    logger.info("User retrieved successfully - id: {}", user_id)
    return resp.ok(data=user)


@router.put("/me")
async def update_user(
    user: UserUpdate,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Update user details.
    """
    logger.info("PUT /user/me - user_id: {}, payload: {}", user_id, user.model_dump())
    db_user = await db_service.get_by_id(session=session, id=user_id)

    if not db_user:
        logger.warning("User not found for update - id: {}", user_id)
        return resp.not_found(message="User not found")

    # Validate and update user
    validator = UserValidator(session=session, data=user)

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
    session: AsyncSession = Depends(get_db_session),
):
    """
    Delete a user by user ID (soft delete).
    """
    logger.info("DELETE /user/me - user_id: {}", user_id)
    user = await db_service.get_by_id(session=session, id=user_id)

    if not user:
        logger.warning("User not found for delete - id: {}", user_id)
        return resp.not_found(message="User not found")

    await db_service.mark_delete_by_id(session=session, id=user_id)
    logger.info("User deleted successfully - id: {}", user_id)
    return resp.ok(message="User deleted successfully")
