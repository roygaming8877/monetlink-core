"""
MonetLink Pydantic Schemas Registry
Defines data structures, types, and validation rules for API inputs and outputs.
"""
from .user import UserCreate, UserLogin, UserResponse, UserUpdate
from .link import LinkCreate, LinkUpdate, LinkResponse
from .view import LinkViewCreate, LinkViewResponse
from .referral import ReferralCreate, ReferralResponse
from .transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from .admin import SystemSettingCreate, SystemSettingUpdate, SystemSettingResponse

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "UserUpdate",
    "LinkCreate", "LinkUpdate", "LinkResponse",
    "LinkViewCreate", "LinkViewResponse",
    "ReferralCreate", "ReferralResponse",
    "TransactionCreate", "TransactionUpdate", "TransactionResponse",
    "SystemSettingCreate", "SystemSettingUpdate", "SystemSettingResponse"
]
