import uuid
from datetime import datetime
from typing import Annotated, Optional

from helpers import validate_email_username, validate_password_strength
from pydantic import BaseModel, EmailStr
from pydantic.functional_validators import AfterValidator

# Define Annotated type aliases with validators
ValidEmail = Annotated[EmailStr, AfterValidator(validate_email_username)]
StrongPassword = Annotated[str, AfterValidator(validate_password_strength)]


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: ValidEmail


class UserCreate(UserBase):
    password: StrongPassword


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOut(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
