from fastapi import APIRouter
from . import auth, developer_api, links, statistics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(links.router, prefix="/links", tags=["Link Management"])
api_router.include_router(developer_api.router, prefix="/tools", tags=["Developer Tools"])
api_router.include_router(statistics.router, prefix="/stats", tags=["Analytics"])
