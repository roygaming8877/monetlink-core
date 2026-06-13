from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.crud.crud_page import custom_page

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home_page(request: Request, db: AsyncSession = Depends(get_async_db)):
    # Fetch live stats for the $220/10000 views counters here
    return templates.TemplateResponse("landing.html", {"request": request})

@router.get("/payout-rates")
async def payout_rates_page(request: Request):
    return templates.TemplateResponse("payout_rates.html", {"request": request})

@router.get("/pages/{slug}")
async def dynamic_legal_pages(slug: str, request: Request, db: AsyncSession = Depends(get_async_db)):
    """Dynamically loads Terms, Privacy, FAQ from the database."""
    page_data = await custom_page.get_by_slug(db, slug=slug)
    if not page_data:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    
    return templates.TemplateResponse("pages/view_page.html", {"request": request, "page": page_data})
  
