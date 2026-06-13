from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime
from app.models.base import MonetLinkBaseModel

class Link(MonetLinkBaseModel):
    __tablename__ = "links"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    # URL Matrix
    original_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    alias: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    domain_used: Mapped[str] = mapped_column(String(100), default="monetlink.online", nullable=False)
    
    # Visibility and Expiry Logic
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Database Relationships
    owner: Mapped["User"] = relationship("User", back_populates="links")
    views: Mapped[List["LinkView"]] = relationship("LinkView", back_populates="link", cascade="all, delete-orphan")
  
