from pydantic import BaseModel, HttpUrl, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
import re

class LinkBase(BaseModel):
    original_url: HttpUrl
    alias: Optional[str] = Field(None, min_length=4, max_length=50, description="Custom alias for the short link")

    @field_validator('alias')
    @classmethod
    def alias_alphanumeric_check(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Alias can only contain letters, numbers, hyphens, and underscores')
        return v

class LinkCreate(LinkBase):
    domain_used: Optional[str] = "monetlink.online"

class LinkUpdate(BaseModel):
    is_hidden: Optional[bool] = None
    original_url: Optional[HttpUrl] = None

class LinkResponse(LinkBase):
    id: str
    user_id: str
    is_hidden: bool
    created_at: datetime
    shortened_url: str  # Dynamically generated during response serialization

    model_config = ConfigDict(from_attributes=True)
  
