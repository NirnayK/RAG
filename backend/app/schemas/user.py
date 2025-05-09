import uuid
from datetime import datetime
from typing import Annotated

from helpers import (
    ValidEmptyString,
    ValidString,
    validate_email_username,
    validate_password_strength,
)
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.functional_validators import AfterValidator

# Define Annotated type aliases with validators
ValidEmail = Annotated[EmailStr, AfterValidator(validate_email_username)]
StrongPassword = Annotated[str, AfterValidator(validate_password_strength)]


class UserBase(BaseModel):
    first_name: ValidString
    last_name: ValidString
    email: ValidEmail


class UserCreate(UserBase):
    password: StrongPassword


class UserUpdate(BaseModel):
    first_name: ValidEmptyString
    last_name: ValidEmptyString


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
