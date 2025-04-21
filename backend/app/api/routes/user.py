from fastapi import APIRouter, Depends, Request
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
        return resp.bad_request(errors=validator.errors, message="Validation failed")

    # Save user to database
    db_user = await validator.save()
    return resp.created(data=db_user, message="User created successfully")


@router.get("/me")
async def get_user(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Get user details by user ID.
    """
    query = select(User).filter(User.id == user_id, User.deleted_at.is_(None))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        return resp.not_found(message="User not found")

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
    query = select(User).filter(User.id == user_id, User.deleted_at.is_(None))
    result = await db.execute(query)
    db_user = result.scalar_one_or_none()

    if not db_user:
        return resp.not_found(message="User not found")

    # Validate and update user
    validator = UserValidator(db=db, data=user)

    if not await validator.is_valid(UPDATE):
        return resp.bad_request(errors=validator.errors, message="Validation failed")

    # Update user
    updated_user = await validator.update(db_user)

    return resp.ok(data=updated_user, message="User updated successfully")


@router.delete("/me")
async def delete_user(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a user by user ID (soft delete).
    """
    query = select(User).filter(User.id == user_id, User.deleted_at.is_(None))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        return resp.not_found(message="User not found")

    await user.mark_deleted(db)
    return resp.ok(message="User deleted successfully")
