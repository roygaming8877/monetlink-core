from sqlalchemy import String, Float, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from app.models.base import MonetLinkBaseModel

class User(MonetLinkBaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Financial Ledger Properties
    wallet_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_earned: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    # Access Control Matrix
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ban_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Billing & Identity Profile
    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address_1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Withdrawal Settings
    preferred_withdrawal_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    withdrawal_account: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship Cascades (One-to-Many)
    links: Mapped[List["Link"]] = relationship("Link", back_populates="owner", cascade="all, delete-orphan")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    invoices: Mapped[List["Invoice"]] = relationship("Invoice", back_populates="user", cascade="all, delete-orphan")
    
    # Self-Referential Relationship for Referrals
    referrals_made: Mapped[List["Referral"]] = relationship("Referral", foreign_keys="[Referral.referrer_id]", back_populates="referrer")
    referred_by: Mapped[Optional["Referral"]] = relationship("Referral", foreign_keys="[Referral.referred_id]", back_populates="referred_user", uselist=False)
  
