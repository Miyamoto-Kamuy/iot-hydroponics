from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routers import auth, device, measurement, websocket, alert, audit_log, user
from app.middleware.audit import AuditMiddleware
from app.core.limiter import limiter


app = FastAPI(
    title="IoT Hydroponics Monitor", 
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=[
        "http://localhost:3000", 
        "https://iot-hydroponics-qqfvjtb9t-poan.vercel.app", 
        "https://iot.poanchen.com"
    ], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)
app.add_middleware(AuditMiddleware)

app.include_router(auth.router)
app.include_router(device.router)
app.include_router(measurement.router)
app.include_router(websocket.router)
app.include_router(alert.router)
app.include_router(audit_log.router)
app.include_router(user.router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/health")
def health_check():
    return {"status": "ok"}