import re

def validate_withdrawal_account(method: str, account_details: str) -> tuple[bool, str]:
    """
    Strictly validates withdrawal destination syntax based on the selected method.
    Prevents failed payouts and admin headaches.
    """
    method_upper = method.upper()

    if method_upper in ["PAYPAL", "BINANCE PAY", "AIRTM"]:
        # Must be a valid email format
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, account_details):
            return False, f"A valid registered email is required for {method}."
            
    elif method_upper == "USDT (TRC20)":
        # Tron wallet addresses usually start with 'T' and are exactly 34 chars
        if not account_details.startswith("T") or len(account_details) != 34:
            return False, "Invalid TRC20 Wallet Address format."
            
    elif method_upper == "UPI":
        # Standard India UPI ID regex validation (e.g., name@okaxis)
        upi_regex = r'^[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}$'
        if not re.match(upi_regex, account_details):
            return False, "Invalid UPI ID format."
            
    elif method_upper in ["PAYTM", "PHONEPE"]:
        # 10 digit Indian phone numbers
        if not re.match(r'^[6-9]\d{9}$', account_details):
            return False, "A valid 10-digit mobile number is required."
            
    return True, "Valid account layout."
  
