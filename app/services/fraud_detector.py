from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.view import LinkView

async def verify_click_authenticity(
    db: AsyncSession, 
    link_id: str, 
    ip_address: str, 
    user_agent: str
) -> bool:
    """
    Enterprise Anti-Fraud validation:
    1. Rejects known bot strings.
    2. Enforces the strict "1 Unique View per IP per 24 Hours" rule.
    """
    # 1. Basic User-Agent Validation
    bad_agents = ["bot", "crawl", "spider", "scraper", "headless"]
    if not user_agent or any(bot in user_agent.lower() for bot in bad_agents):
        return False

    # 2. 24-Hour Unique IP Validation Window
    time_threshold = datetime.utcnow() - timedelta(hours=24)
    
    query = select(func.count(LinkView.id)).where(
        LinkView.link_id == link_id,
        LinkView.ip_address == ip_address,
        LinkView.created_at >= time_threshold
    )
    
    result = await db.execute(query)
    recent_views = result.scalar_one() or 0

    # If the IP has viewed this link in the last 24h, the click is invalid for payment
    if recent_views > 0:
        return False

    return True
  
