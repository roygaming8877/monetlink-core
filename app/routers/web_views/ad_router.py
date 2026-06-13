from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.crud.crud_link import link
from app.services.fraud_detector import verify_click_authenticity
from app.services.cpm_engine import calculate_cpm_payout

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/{alias}")
async def step_1_entry_gate(alias: str, request: Request, db: AsyncSession = Depends(get_async_db)):
    """Step 1: Captcha / Initial landing wall to block bots."""
    db_link = await link.get_by_alias(db, alias=alias)
    if not db_link or db_link.is_hidden:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    
    return templates.TemplateResponse("ad_flow/step1_captcha.html", {"request": request, "alias": alias})

@router.get("/validate/article/{alias}")
async def step_2_article_buffer(alias: str, request: Request):
    """Step 2: The content buffer page (simulated blog) for premium ad-network compliance."""
    return templates.TemplateResponse("ad_flow/step2_article.html", {"request": request, "alias": alias})

@router.get("/go/{alias}")
async def step_3_final_redirection(alias: str, request: Request, db: AsyncSession = Depends(get_async_db)):
    """Step 3: Verification, Financial Credit, and Target Redirection."""
    db_link = await link.get_by_alias(db, alias=alias)
    if not db_link:
        raise HTTPException(status_code=404, detail="Link expired.")

    # Execute backend telemetry tracing (IP, Country, User-Agent)
    ip_address = request.headers.get("X-Forwarded-For", "127.0.0.1").split(",")[0]
    user_agent = request.headers.get("User-Agent", "")
    country_code = getattr(request.state, "country", "XX")

    # Anti-Fraud Verification Pipeline
    is_genuine = await verify_click_authenticity(db, db_link.id, ip_address, user_agent)
    
    if is_genuine:
        # Calculate exactly how much this click pays based on visitor origin
        payout = await calculate_cpm_payout(db, country_code)
        
        # PUSH TO BACKGROUND WORKER: In production, send this via Celery so DB isn't blocked
        # celery_app.send_task("process_valid_click", args=[db_link.id, ip_address, country_code, payout])
        pass

    # Finally safely route the user to their requested destination
    return RedirectResponse(url=db_link.original_url, status_code=302)
  
