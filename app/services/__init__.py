"""
MonetLink Business Services Registry
Handles pure business logic: CPM calculation, Fraud detection, Referral cuts, and Ad-Flow states.
"""
from .cpm_engine import calculate_cpm_payout
from .fraud_detector import verify_click_authenticity
from .referral_engine import process_referral_commission
from .ad_flow_manager import verify_ad_flow_state
from .payment_validator import validate_withdrawal_account
from .script_generator import generate_full_page_script

__all__ = [
    "calculate_cpm_payout",
    "verify_click_authenticity",
    "process_referral_commission",
    "verify_ad_flow_state",
    "validate_withdrawal_account",
    "generate_full_page_script"
]
