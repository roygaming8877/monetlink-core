from sqlalchemy import String, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import MonetLinkBaseModel

class Referral(MonetLinkBaseModel):
    __tablename__ = "referrals"
    
    __table_args__ = (
        Index("ix_referrals_referrer_referred", "referrer_id", "referred_id", unique=True),
    )

    referrer_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    referred_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Commission Tracking Matrix
    total_commission_earned: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    referrer: Mapped["User"] = relationship("User", foreign_keys=[referrer_id], back_populates="referrals_made")
    referred_user: Mapped["User"] = relationship("User", foreign_keys=[referred_id], back_populates="referred_by")
  
