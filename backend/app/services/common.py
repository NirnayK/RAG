from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Sequence, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class CommonService(BaseModel):

    def __init__(self, model: Any):
        self.model = model

    # GET DB QUERIES
    async def get_by_id(self, session: AsyncSession, id: UUID) -> Optional[Any]:
        """
        Get a record by its ID.
        """
        query = select(self.model).filter(self.model.id == id, self.model.deleted_at.is_(None))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_field(self, session: AsyncSession, field: str, value: Any) -> Optional[Any]:
        """
        Get a record by a specific field.
        """
        query = select(self.model).filter(getattr(self.model, field) == value, self.model.deleted_at.is_(None))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, session: AsyncSession, **filters: Any) -> Optional[Sequence[Any]]:
        """
        Get all records or filter by a specific field.
        """
        formatted_filters = {getattr(self.model, key): value for key, value in filters.items()}
        if formatted_filters:
            query = select(self.model).filter(*formatted_filters, self.model.deleted_at.is_(None))
        else:
            query = select(self.model).filter(self.model.deleted_at.is_(None))
        result = await session.execute(query)
        return result.scalars().all()

    # UPDATE DB QUERIES
    async def update_by_id(self, session: AsyncSession, id: UUID, **kwargs) -> Optional[Any]:
        """
        Update a record by its ID.
        """
        query = select(self.model).filter(self.model.id == id)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
            await session.commit()
            return record
        return None

    async def update_many(self, session: AsyncSession, filters: dict, updates: dict) -> bool:
        """
        Bulk update records using raw SQL.
        """
        formatted_filters = {getattr(self.model, key): value for key, value in filters.items()}
        stmt = update(self.model).where(formatted_filters).values(**updates)
        await session.execute(stmt)
        await session.commit()
        return True

    async def mark_delete_by_id(self, session: AsyncSession, id: UUID) -> bool:
        """
        Mark a record as deleted by its ID.
        """
        query = select(self.model).filter(self.model.id == id)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        if record:
            record.deleted_at = datetime.now(timezone.utc)
            await session.commit()
            return True
        return False

    async def delete_by_id(self, session: AsyncSession, id: UUID) -> bool:
        """
        Delete a record by its ID.
        """
        query = select(self.model).filter(self.model.id == id)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        if record:
            await session.delete(record)
            await session.commit()
            return True
        return False

    async def delete_many(self, session: AsyncSession, filters: dict) -> bool:
        """
        Bulk delete records using raw SQL.
        """
        formatted_filters = {getattr(self.model, key): value for key, value in filters.items()}
        stmt = delete(self.model).where(formatted_filters)
        await session.execute(stmt)
        await session.commit()
        return True
