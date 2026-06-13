from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128, description="Must be at least 8 characters long")
    re_enter_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserCreate':
        if self.password != self.re_enter_password:
            raise ValueError('Passwords do not match')
        return self

class UserLogin(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    address_1: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    country_code: Optional[str] = Field(None, min_length=2, max_length=2)
    phone_number: Optional[str] = Field(None, max_length=20)
    preferred_withdrawal_method: Optional[str] = Field(None, max_length=50)
    withdrawal_account: Optional[str] = None

class UserResponse(UserBase):
    id: str
    wallet_balance: float
    total_earned: float
    is_active: bool
    is_banned: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
  
