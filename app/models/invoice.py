from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import MonetLinkBaseModel

class Invoice(MonetLinkBaseModel):
    __tablename__ = "invoices"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    transaction_id: Mapped[str] = mapped_column(String(36), ForeignKey("transactions.id", ondelete="SET NULL"), nullable=True)
    
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="paid", nullable=False)
    invoice_pdf_url: Mapped[str] = mapped_column(String(512), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="invoices")
  
