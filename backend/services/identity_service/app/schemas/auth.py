
from typing import Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
)


class RegisterRequest(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    password: SecretStr

    organization_name: str = Field(
        min_length=2,
        max_length=150,
    )

    organization_slug: str = Field(
        min_length=3,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    @field_validator(
        "full_name",
        "organization_name",
        mode="before",
    )
    @classmethod
    def strip_names(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return str(value).lower()

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: SecretStr,
    ) -> SecretStr:
        password = value.get_secret_value()

        if not 12 <= len(password) <= 128:
            raise ValueError(
                "Password must contain 12 to 128 characters"
            )

        return value


class RegisterResponse(BaseModel):
    user_id: UUID
    organization_id: UUID
    email: EmailStr
    full_name: str
    role: Literal["owner"]
