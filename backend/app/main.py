from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, device, measurement, websocket, alert
from app.middleware.audit import AuditMiddleware

app = FastAPI(
    title="IoT Hydroponics Monitor", 
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000"], 
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

@app.get("/health")
def health_check():
    return {"status": "ok"}