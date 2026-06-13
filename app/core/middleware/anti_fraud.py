from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

class AntiFraudMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_agent = request.headers.get("user-agent", "").lower()
        # Legitimate block against headless scrapers hurting your server
        if "python-requests" in user_agent or "curl" in user_agent:
            return JSONResponse(status_code=403, content={"error": "Automated requests denied."})
        
        response = await call_next(request)
        return response
      
