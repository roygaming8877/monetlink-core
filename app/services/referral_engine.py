import hashlib
from datetime import datetime
from app.core.config import settings

def generate_flow_token(alias: str, step: int, ip_address: str) -> str:
    """
    Generates a fast, stateless cryptographic hash to ensure users cannot skip 
    ad-pages (e.g., jumping directly to step 3 without viewing step 1).
    """
    # Combines current hour with IP and Alias to make a time-sensitive, user-specific token
    time_block = datetime.utcnow().strftime("%Y-%m-%d-%H")
    raw_string = f"{alias}:{step}:{ip_address}:{time_block}:{settings.SECRET_KEY}"
    return hashlib.sha256(raw_string.encode()).hexdigest()

def verify_ad_flow_state(alias: str, expected_step: int, ip_address: str, provided_token: str) -> bool:
    """
    Validates if the user's provided token matches the required state.
    """
    expected_token = generate_flow_token(alias, expected_step, ip_address)
    return expected_token == provided_token
  
