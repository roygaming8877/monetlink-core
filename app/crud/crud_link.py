from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.link import Link
from app.schemas.link import LinkCreate, LinkUpdate

class CRUDLink(CRUDBase[Link, LinkCreate, LinkUpdate]):
    async def get_by_alias(self, db: AsyncSession, *, alias: str) -> Optional[Link]:
        """High-speed routing check for alias resolution."""
        query = select(Link).where(Link.alias == alias)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_multi_by_owner(self, db: AsyncSession, *, user_id: str, skip: int = 0, limit: int = 100) -> List[Link]:
        """Fetches paginated links strictly for the logged-in user dashboard."""
        query = select(Link).where(Link.user_id == user_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

link = CRUDLink(Link)
