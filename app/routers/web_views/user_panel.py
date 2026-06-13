from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def member_dashboard(request: Request):
    """Renders the main graphical dashboard with the 4 top metrics."""
    # Requires session validation in production
    return templates.TemplateResponse("member/dashboard.html", {"request": request})

@router.get("/withdraw")
async def member_withdraw_desk(request: Request):
    return templates.TemplateResponse("member/withdraw.html", {"request": request})
  
