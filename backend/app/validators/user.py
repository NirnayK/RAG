from collections import defaultdict
from typing import Dict, List, Tuple, Union

from passlib.context import CryptContext

from models import User
from schemas.user import UserCreate, UserUpdate
from validators.base import BaseValidator

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserValidator(BaseValidator[Union[UserCreate, UserUpdate]]):
    """
    Validator for user-related operations.
    """

    class Config:
        model_class = User

    async def save_validate(self) -> Tuple[bool, Dict[str, List[str]]]:
        """
        Validate user data based on operation
        """
        errors = defaultdict(list)
        query = self.validate_is_unique(User, "email", self.data.email)
        result = await self.session.execute(query)

        if not result:
            errors["email"].append("Email already exists")

        return True, errors

    async def save_serialize(self) -> Dict:
        """
        Prepare user data for saving, including password hashing
        """
        data = self.serialize()

        # Hash password for UserCreate schemas
        data["password"] = pswd_context.hash(data["password"])

        return data
