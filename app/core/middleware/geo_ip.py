from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class GeoIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Read Cloudflare's country header
        country = request.headers.get("CF-IPCountry", "Global")
        request.state.country = country
        response = await call_next(request)
        return response
      
