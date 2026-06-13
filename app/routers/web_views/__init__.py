from fastapi import APIRouter
from . import ad_router, admin_matrix, public, user_panel

web_router = APIRouter()

web_router.include_router(public.router, tags=["Public Pages"])
web_router.include_router(user_panel.router, prefix="/member", tags=["Member Dashboard"])
web_router.include_router(admin_matrix.router, prefix="/admin", tags=["Administration"])
web_router.include_router(ad_router.router, tags=["Ad Redirection Flow"])
