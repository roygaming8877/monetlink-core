from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class SystemSettingBase(BaseModel):
    key: str = Field(..., max_length=100)
    value: str
    description: Optional[str] = None
    data_type: str = Field(default="string", pattern="^(string|float|json|boolean)$")

class SystemSettingCreate(SystemSettingBase):
    pass

class SystemSettingUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None

class SystemSettingResponse(SystemSettingBase):
    id: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
  
