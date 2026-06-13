"""
MonetLink Enterprise Database Models Registry
Exposes all SQLAlchemy ORM models for Alembic migrations and application routing.
"""
from app.models.base import MonetLinkBaseModel
from app.models.user import User
from app.models.link import Link
from app.models.view import LinkView
from app.models.referral import Referral
from app.models.transaction import Transaction
from app.models.page import CustomPage
from app.models.invoice import Invoice
from app.models.setting import SystemSetting

# Ensures all models are loaded into the declarative base metadata
__all__ = [
    "MonetLinkBaseModel",
    "User",
    "Link",
    "LinkView",
    "Referral",
    "Transaction",
    "CustomPage",
    "Invoice",
    "SystemSetting",
]
