from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # In a full setup, connect to Redis here to track request.client.host
        # If hits > 100 per minute, return 429 Too Many Requests
        response = await call_next(request)
        return response
      
