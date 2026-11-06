
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    confirm_password: str = Field(min_length=8, max_length=72)

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        if not any(c.isupper() for c in self.password):
            raise ValueError("Password must contain an uppercase letter")

        if not any(c.islower() for c in self.password):
            raise ValueError("Password must contain a lowercase letter")

        if not any(c.isdigit() for c in self.password):
            raise ValueError("Password must contain a number")

        if not any(not c.isalnum() for c in self.password):
            raise ValueError("Password must contain a special character")

        return self


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    message: str


class TokenVerificationResponse(BaseModel):
    valid: bool
    message: str
    user_id: int | None = None
    role: str | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=72)
    new_password: str = Field(min_length=8, max_length=72)

    @model_validator(mode="after")
    def validate_new_password(self):
        password = self.new_password

        if not any(c.isupper() for c in password):
            raise ValueError("New password must contain an uppercase letter")
        if not any(c.islower() for c in password):
            raise ValueError("New password must contain a lowercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("New password must contain a number")
        if not any(not c.isalnum() for c in password):
            raise ValueError("New password must contain a special character")
        if password == self.current_password:
            raise ValueError("New password must differ from current password")

        return self
