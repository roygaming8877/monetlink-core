# links.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.schemas.link import LinkCreate, LinkResponse

router = APIRouter()

@router.post("/shorten", response_model=LinkResponse)
async def shorten_url(payload: LinkCreate, db: AsyncSession = Depends(get_async_db)):
    """Internal endpoint used by the dashboard UI to generate links."""
    # Production injection happens here
    pass
