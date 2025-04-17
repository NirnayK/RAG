import asyncio
from abc import ABC
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseValidator(ABC):
    """
    Base class for validators.
    """

    class Config:
        model_class = None  # Set by subclasses

    def __init__(self, db: AsyncSession, data: BaseModel, user_id: str = ""):
        self.data = data
        self.db = db
        self.user_id = user_id
        self.errors = []  # Store validation errors as a list of strings

    def validate_exist(self, model: Any, pk: str):
        return select(model).filter(model.id == pk).exists()

    def validate_is_owner(self, model: Any, pk: str):
        return select(model).filter(model.id == pk, model.user_id == self.user_id).exists()

    def validate_is_unique(self, model: Any, col: str, value: Any):
        return select(model).filter(getattr(model, col) == value).exists()

    async def validate_queries(self, db_queries: List, apis: List[Callable]):
        tasks = [self.db.execute(query) for query in db_queries]
        tasks += [api() for api in apis]
        results = await asyncio.gather(*tasks)
        return results

    async def validate(self) -> Tuple[bool, Dict[str, List[str]]]:
        """
        Validate the data and return a tuple of (is_valid, errors).
        This is a base implementation that returns valid with no errors.
        Subclasses should override this but can call super().validate()

        Returns:
            Tuple[bool, Dict[str, List[str]]]: A tuple containing:
                - is_valid: True if validation passed, False otherwise
                - errors: A dictionary of field names and their error messages
        """
        return True, {}

    async def is_valid(self) -> bool:
        """
        Check if the data is valid.

        Returns:
            bool: True if the data is valid

        Side effects:
            Populates self.errors list when validation fails
        """
        is_valid, error_dict = await self.validate()
        if not is_valid:
            # Convert error dictionary to a list of error messages
            for field, messages in error_dict.items():
                if isinstance(messages, list):
                    for msg in messages:
                        self.errors.append(f"{field}: {msg}")
                else:
                    self.errors.append(f"{field}: {messages}")
            return False
        return True

    def serialize(self, exclude: Optional[Set[str]] = None) -> Dict:
        """
        Serialize the data model to a dictionary.

        Args:
            exclude: Optional set of field names to exclude from serialization

        Returns:
            Dict: Serialized data
        """
        # For Pydantic v2
        return self.data.model_dump(exclude=exclude or set())
        # For Pydantic v1 use: return self.data.dict(exclude=exclude or set())

    async def save_serialize(self) -> Dict:
        """
        Prepare data for saving to database.
        By default uses the serialize() method, but can be overridden
        for custom save serialization logic.

        Returns:
            Dict: Serialized data ready for database insertion
        """
        return self.serialize()

    async def save(self) -> Any:
        """
        Save the data as a new database record using the configured model class.

        Returns:
            The created database model instance
        """
        if not self.Config.model_class:
            raise ValueError("model_class must be set in Config")

        data = await self.save_serialize()
        db_obj = self.Config.model_class(**data)
        self.db.add(db_obj)
        await self.db.commit()
        return db_obj

    async def update_serialize(self, db_obj: Any) -> Dict:
        """
        Prepare data for updating an existing database record.
        By default uses the serialize() method, but can be overridden
        for custom update serialization logic.

        Args:
            db_obj: The database object to update (may be used for conditional logic)

        Returns:
            Dict: Serialized data ready for database update
        """
        return self.serialize()

    async def update(self, db_obj: Any, partial: bool = True) -> Any:
        """
        Update an existing database record using the serialized data.

        Args:
            db_obj: The database object to update
            partial: If True, only update specified fields

        Returns:
            The updated database model instance
        """
        data = await self.update_serialize(db_obj)

        if partial:
            # Only update fields that are provided
            for field, value in data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
        else:
            # Full update - set all fields from the model
            for field in db_obj.__table__.columns.keys():
                if field in data:
                    setattr(db_obj, field, data[field])

        await self.db.commit()
        return db_obj
