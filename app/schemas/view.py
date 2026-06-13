from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class LinkViewBase(BaseModel):
    ip_address: str
    country: str = Field(default="Global", max_length=2)
    user_agent: Optional[str] = None
    referer: Optional[str] = None
    fingerprint: Optional[str] = None

class LinkViewCreate(LinkViewBase):
    link_id: str
    is_valid: bool = True
    payout_credited: float = 0.0
    cpm_applied: float = 0.0

class LinkViewResponse(LinkViewBase):
    id: str
    link_id: str
    is_valid: bool
    payout_credited: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
  
