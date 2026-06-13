from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ReferralBase(BaseModel):
    referrer_id: str
    referred_id: str

class ReferralCreate(ReferralBase):
    pass

class ReferralResponse(ReferralBase):
    id: str
    total_commission_earned: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
  
