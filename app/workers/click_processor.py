import asyncio
from celery import shared_task
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.view import LinkView
from app.models.link import Link
from app.models.user import User
from app.models.referral import Referral
from app.services.cpm_engine import calculate_cpm_payout

async def _async_process_click_ledger(link_id: str, ip_address: str, country: str, user_agent: str, payout: float):
    """Isolated async function to execute the financial ledger transaction."""
    async with AsyncSessionLocal() as db:
        try:
            # 1. Fetch Link and Owner Details safely
            link_query = select(Link).where(Link.id == link_id)
            link_result = await db.execute(link_query)
            db_link = link_result.scalar_one_or_none()
            if not db_link: return

            # 2. Record the View Telemetry
            new_view = LinkView(
                link_id=db_link.id,
                ip_address=ip_address,
                country=country,
                user_agent=user_agent,
                is_valid=True,
                payout_credited=payout,
                cpm_applied=(payout * 1000)
            )
            db.add(new_view)

            # 3. Credit the Publisher Wallet (Atomic Operation)
            owner_query = select(User).where(User.id == db_link.user_id).with_for_update() # Locks row for secure balance update
            owner_res = await db.execute(owner_query)
            owner = owner_res.scalar_one_or_none()
            
            if owner:
                owner.wallet_balance += payout
                owner.total_earned += payout
                
                # 4. Referral System Engine (20% Lifetime cut)
                ref_query = select(Referral).where(Referral.referred_id == owner.id)
                ref_res = await db.execute(ref_query)
                referral_rel = ref_res.scalar_one_or_none()
                
                if referral_rel:
                    ref_commission = payout * 0.20
                    referral_rel.total_commission_earned += ref_commission
                    
                    referrer_query = select(User).where(User.id == referral_rel.referrer_id)
                    referrer_res = await db.execute(referrer_query)
                    master_referrer = referrer_res.scalar_one_or_none()
                    
                    if master_referrer:
                        master_referrer.wallet_balance += ref_commission
                        master_referrer.total_earned += ref_commission

            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e

@shared_task(name="workers.process_valid_click_task", bind=True, max_retries=3)
def process_valid_click_task(self, link_id: str, ip_address: str, country: str, user_agent: str, payout: float):
    """Celery Task Wrapper for asynchronous background execution."""
    try:
        asyncio.run(_async_process_click_ledger(link_id, ip_address, country, user_agent, payout))
        return f"Successfully processed click ledger for link {link_id}"
    except Exception as exc:
        self.retry(exc=exc, countdown=5) # Retries 3 times after 5 seconds if DB is locked
