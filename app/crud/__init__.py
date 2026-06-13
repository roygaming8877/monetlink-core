"""
MonetLink CRUD (Create, Read, Update, Delete) Registry
Centralized data access objects for asynchronous database operations.
"""
from .crud_user import user
from .crud_link import link
from .crud_view import link_view
from .crud_referral import referral
from .crud_transaction import transaction
from .crud_page import custom_page
from .crud_setting import system_setting

__all__ = [
    "user",
    "link",
    "link_view",
    "referral",
    "transaction",
    "custom_page",
    "system_setting"
]
