from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base import MonetLinkBaseModel

class SystemSetting(MonetLinkBaseModel):
    __tablename__ = "system_settings"

    key: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=True)
    
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    data_type: Mapped[str] = mapped_column(String(20), default="string", nullable=False) # 'string', 'float', 'json', 'boolean'
