import asyncio
from datetime import datetime, timedelta
from celery import shared_task
from sqlalchemy import select, update, func
from app.core.database import AsyncSessionLocal
from app.models.view import LinkView

async def _async_sweep_fraudulent_clicks():
    """Retroactive fraud sweep. Identifies IP addresses with abnormal click velocities."""
    async with AsyncSessionLocal() as db:
        time_threshold = datetime.utcnow() - timedelta(hours=1)
        
        # Identify IPs generating more than 15 clicks an hour across the platform
        fraud_query = select(LinkView.ip_address).where(
            LinkView.created_at >= time_threshold,
            LinkView.is_valid == True
        ).group_by(LinkView.ip_address).having(func.count(LinkView.id) > 15)
        
        fraud_result = await db.execute(fraud_query)
        suspicious_ips = fraud_result.scalars().all()
        
        if suspicious_ips:
            # Mark all recent clicks from these IPs as invalid to trigger deduction audits later
            stmt = update(LinkView).where(
                LinkView.ip_address.in_(suspicious_ips),
                LinkView.created_at >= time_threshold
            ).values(is_valid=False)
            
            await db.execute(stmt)
            await db.commit()
            
        return len(suspicious_ips)

@shared_task(name="workers.sweep_fraudulent_clicks_task")
def sweep_fraudulent_clicks_task():
    """Runs periodic offline fraud scans."""
    flagged_count = asyncio.run(_async_sweep_fraudulent_clicks())
    return f"Fraud sweep completed. Flagged {flagged_count} IPs."
  
