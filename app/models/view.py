from sqlalchemy import String, Float, Boolean, ForeignKey, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.models.base import MonetLinkBaseModel

class LinkView(MonetLinkBaseModel):
    __tablename__ = "link_views"
    
    # Composite indexing for heavy read/write analytics operations
    __table_args__ = (
        Index("ix_link_views_link_id_ip", "link_id", "ip_address"),
        Index("ix_link_views_created_country", "created_at", "country"),
    )

    link_id: Mapped[str] = mapped_column(String(36), ForeignKey("links.id", ondelete="CASCADE"), nullable=False)
    
    # Traffic Telemetry & Anti-Fraud Identification
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    country: Mapped[str] = mapped_column(String(2), default="XX", nullable=False)
    fingerprint: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    referer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Monetization Metrics
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, doc="False if flagged by anti-fraud engine")
    payout_credited: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cpm_applied: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    link: Mapped["Link"] = relationship("Link", back_populates="views")
  
