from fastapi import Request
from fastapi.responses import JSONResponse

class FraudDetectedException(Exception):
    def __init__(self, message: str):
        self.message = message

async def fraud_exception_handler(request: Request, exc: FraudDetectedException):
    return JSONResponse(
        status_code=403,
        content={"detail": f"Security Policy Violation: {exc.message}"},
    )
  
