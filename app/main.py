"""
MonetLink Enterprise SaaS - Main Application Entry Point
Initializes the FastAPI framework, binds middlewares, mounts static files, 
and connects all APIRouters to the global execution context.
"""

import time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import fraud_exception_handler, FraudDetectedException
from app.routers.api_v1 import api_router
from app.routers.web_views import web_router
from app.core.middleware.anti_fraud import AntiFraudMiddleware
from app.core.middleware.geo_ip import GeoIPMiddleware

# =====================================================================
# 1. ENTERPRISE LOGGING INITIALIZATION
# =====================================================================
setup_logging()

def create_monetlink_engine() -> FastAPI:
    """Factory pattern to construct and configure the MonetLink FastAPI instance."""
    
    # Initialize Core Application
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="2.0.0-enterprise",
        description="High-Performance URL Shortener, Ad-Routing, and CPM Monetization Engine.",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        # Disabling Swagger UI in production to hide internal API structures from hackers
        docs_url=None, 
        redoc_url=None
    )

    # Mount Static Assets (CSS, JS, Fonts, Images)
    # The 'static' folder must exist in the root 'app' directory
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # =====================================================================
    # 2. MIDDLEWARE STACK BINDING (Order matters!)
    # =====================================================================
    
    # CORS (Cross-Origin Resource Sharing) - Restricts which domains can hit the headless API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_DOMAINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
    )
    
    # Session Manager for Jinja2 Template Flash Messages and Admin States
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
    
    # Custom MonetLink Enterprise Middlewares
    app.add_middleware(GeoIPMiddleware)      # Extracts Cloudflare Country headers for CPM calculation
    app.add_middleware(AntiFraudMiddleware)  # Blocks basic headless scrapers globally

    # Server Response Time Telemetry Injector
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time-Sec"] = str(round(process_time, 4))
        response.headers["X-Server-Engine"] = "MonetLink-Overlord-v2"
        return response

    # =====================================================================
    # 3. GLOBAL EXCEPTION HANDLERS
    # =====================================================================
    app.add_exception_handler(FraudDetectedException, fraud_exception_handler)

    # =====================================================================
    # 4. ROUTER MATRIX INCLUSION
    # =====================================================================
    
    # Headless RESTful API Routes (Used by internal dashboard scripts or external devs)
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Server-Side Rendered Web Views (Landing pages, ad-flows, and user/admin dashboards)
    app.include_router(web_router)

    return app

# =====================================================================
# SERVER LAUNCHER
# =====================================================================
app = create_monetlink_engine()

@app.on_event("startup")
async def startup_event():
    """Boot sequence execution."""
    print(f"🚀 [{settings.PROJECT_NAME}] Engine Core Booting Up...")
    print("🛡️ Anti-Fraud Shield Matrix: ONLINE")
    print("⚡ Geo-Routing Ad Nodes: ACTIVE")
    print("🌐 System ready to accept highly concurrent traffic.")

@app.on_event("shutdown")
async def shutdown_event():
    """Graceful degradation and resource cleanup sequence."""
    print(f"🛑 [{settings.PROJECT_NAME}] Terminating database connections.")
    print("🛑 Engine Shutting Down Safely. Goodbye.")

