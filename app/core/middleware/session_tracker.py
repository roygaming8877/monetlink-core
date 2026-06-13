from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SessionTrackerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Attaches a unique session ID to track normal user flows
        session_id = request.cookies.get("ml_session")
        request.state.session_id = session_id
        response = await call_next(request)
        return response
      
