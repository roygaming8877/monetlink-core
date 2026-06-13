from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.view import LinkView
from app.schemas.view import LinkViewCreate, LinkViewBase

class CRUDLinkView(CRUDBase[LinkView, LinkViewCreate, LinkViewBase]):
    async def count_valid_views_for_link(self, db: AsyncSession, *, link_id: str) -> int:
        """Returns total genuine (is_valid=True) views for a specific link."""
        query = select(func.count(LinkView.id)).where(
            LinkView.link_id == link_id, 
            LinkView.is_valid == True
        )
        result = await db.execute(query)
        return result.scalar_one() or 0

link_view = CRUDLinkView(LinkView)
