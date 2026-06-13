from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.crud.crud_link import link
from app.schemas.link import LinkCreate
# Assume get_current_user_from_token is a standard OAuth2 dependency
# from app.api.deps import get_current_user_from_token 

router = APIRouter()

@router.get("/api")
async def quick_shorten_api(
    api: str = Query(..., description="Developer API Token"),
    url: str = Query(..., description="Destination URL to shorten"),
    alias: str = Query(None, description="Custom Alias"),
    format: str = Query("json", description="Response format (json or text)"),
    db: AsyncSession = Depends(get_async_db)
):
    """MonetLink Quick Link & Developer API implementation."""
    # In production, validate the 'api' token against the users table here
    # user = await get_user_by_api_token(db, api)
    
    link_in = LinkCreate(original_url=url, alias=alias)
    
    try:
        # Pass a mocked user_id for now until dependencies are fully linked
        new_link = await link.create(db, obj_in=link_in) # Requires user injection in production
        short_url = f"https://monetlink.online/{new_link.alias}"
        
        if format.lower() == "text":
            return PlainTextResponse(content=short_url)
        
        return JSONResponse(content={"status": "success", "shortenedUrl": short_url})
        
    except Exception as e:
        if format.lower() == "text":
            return PlainTextResponse(content="error")
        return JSONResponse(content={"status": "error", "message": "Alias taken or invalid URL."})
      
