from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float = Field(gt=0, description="Transaction amount must be strictly positive")
    payment_method: str

class TransactionCreate(TransactionBase):
    payment_account: str

    @model_validator(mode='after')
    def validate_minimum_withdrawal(self) -> 'TransactionCreate':
        if self.amount < 5.00:
            raise ValueError('Minimum withdrawal threshold is $5.00')
        return self

class TransactionUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(pending|approved|rejected|completed)$")
    admin_notes: Optional[str] = None
    tx_hash_or_receipt: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: str
    user_id: str
    transaction_type: str
    status: str
    payment_account: str
    admin_notes: Optional[str]
    tx_hash_or_receipt: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
  
