from sqlalchemy import String, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.models.base import MonetLinkBaseModel

class Transaction(MonetLinkBaseModel):
    __tablename__ = "transactions"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(50), default="withdrawal", nullable=False) # e.g., 'withdrawal', 'bonus'
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False) # 'pending', 'approved', 'rejected', 'completed'
    
    # Payment Vector Information
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    payment_account: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Administration Notes
    admin_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tx_hash_or_receipt: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="transactions")
  
