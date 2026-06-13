from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base import MonetLinkBaseModel

class CustomPage(MonetLinkBaseModel):
    __tablename__ = "custom_pages"

    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False) # HTML or Markdown content
    
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    meta_description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
  
