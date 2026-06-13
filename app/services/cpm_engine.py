from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.crud.crud_setting import system_setting

async def calculate_cpm_payout(db: AsyncSession, country_code: str) -> float:
    """
    Dynamically calculates the exact payout amount for a single valid click 
    based on the visitor's country.
    Formula: (CPM Rate / 1000)
    """
    # In a fully cached system, this would read from Redis first.
    # We fallback to environment defaults if database dynamic settings aren't set yet.
    
    country_upper = country_code.upper()
    cpm_rate = settings.DEFAULT_CPM_GLOBAL

    if country_upper in ["US", "USA"]:
        cpm_rate = settings.DEFAULT_CPM_USA
    elif country_upper in ["IN", "IND"]:
        cpm_rate = settings.DEFAULT_CPM_INDIA
    elif country_upper in ["CA", "GB", "AU"]:
        cpm_rate = 9.00  # Example Tier 1 fallback
        
    # Optional: Fetch dynamic override from admin settings table
    # dynamic_rate = await system_setting.get_by_key(db, f"CPM_{country_upper}")
    # if dynamic_rate: cpm_rate = float(dynamic_rate.value)

    # Convert CPM (Cost Per Mille/1000) to a single click value
    single_click_payout = cpm_rate / 1000.0
    return round(single_click_payout, 6)
  
