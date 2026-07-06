import asyncio
import random
from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Device, Measurement, Alert, User
from app.core.security import verify_access_token
from app.core.exceptions import forbidden, not_found

router = APIRouter()

ALERT_RULES = {
    "temperature": {"max": 35, "min": 10}, 
    "humidity": {"max": 90, "min": 20}, 
    "ph": {"max": 8.0, "min": 5.5},
    "water_level": {"max": 100, "min": 10},  
}

SENSOR_TYPE = [
    {"type": "temperature", "unit": "°C", "range": (15, 40)},
    {"type": "humidity", "unit": "%", "range": (15, 95)},
    {"type": "ph", "unit": "pH", "range": (4.0, 9.0)},
    {"type": "water_level", "unit": "%", "range": (5, 100)},
]

def _get_current_user_ws(token: str, db: Session) -> User:
    payload = verify_access_token(token)
    if not payload:
        return None
    user_id = payload.get("user_id")
    return db.query(User).filter(User.id == user_id).first()

@router.websocket("/ws/devices/{device_id}")
async def device_websocket(
    websocket: WebSocket, 
    device_id: int, 
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    user = _get_current_user_ws(token, db)
    if not user:
        await websocket.close(code=4001)
        return
    
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        await websocket.close(code=4004)
        return
    
    if user.role != "admin" and device.created_by != user.id:
        await websocket.close(code=4003)
        return
    
    await websocket.accept()

    try:
        sensor_index = 0
        while True:
            sensor = SENSOR_TYPE[sensor_index % len(SENSOR_TYPE)]
            value = round(random.uniform(*sensor["range"]), 2)

            measurement = Measurement(
                device_id=device_id,
                sensor_type=sensor["type"], 
                value=value, 
                unit=sensor["unit"]
            )
            db.add(measurement)

            rule = ALERT_RULES.get(sensor["type"])
            if rule and (value > rule["max"] or value < rule["min"]):
                alert = Alert(
                    device_id=device_id,
                    sensor_type=sensor["type"], 
                    message=f"{sensor['type']} value {value}{sensor['unit']} out of range ({rule['min']} - {rule['max']})",
                    status="unread",
                )
                db.add(alert)

            device.last_seen_at = datetime.now(timezone.utc)
            device.status = "online"
            db.commit()

            await websocket.send_json({
                "device_id":device_id,
                "sensor_type":sensor["type"], 
                "value":value, 
                "unit":sensor["unit"], 
                "recorded_at": datetime.now(timezone.utc).isoformat()
            })

            sensor_index += 1
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        device.status = "offline"
        db.commit()

@router.websocket("/ws/dashboard")
async def devices_websocket(
    websocket: WebSocket,     
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    user = _get_current_user_ws(token, db)
    if not user:
        await websocket.close(code=4001)
        return
    
    devices = db.query(Device)
    if user.role != "admin":        
        devices = devices.filter(Device.created_by == user.id)
    devices = devices.all()
    
    await websocket.accept()
    if not devices:
        await websocket.send_json({
            "message": "no devices found"
        })
        await websocket.close(code=1000)
        return        

    try:
        sensor_index = 0
        while True:
            device=devices[sensor_index % len(devices)]
            sensor = SENSOR_TYPE[sensor_index % len(SENSOR_TYPE)]
            value = round(random.uniform(*sensor["range"]), 2)

            measurement = Measurement(
                device_id=device.id,
                sensor_type=sensor["type"], 
                value=value, 
                unit=sensor["unit"]
            )
            db.add(measurement)

            rule = ALERT_RULES.get(sensor["type"])
            if rule and (value > rule["max"] or value < rule["min"]):
                alert = Alert(
                    device_id=device.id,
                    sensor_type=sensor["type"], 
                    message=f"{sensor['type']} value {value}{sensor['unit']} out of range ({rule['min']} - {rule['max']})",
                    status="unread",
                )
                db.add(alert)

            device.last_seen_at = datetime.now(timezone.utc)
            device.status = "online"
            db.commit()

            await websocket.send_json({
                "device_id":device.id,
                "sensor_type":sensor["type"], 
                "value":value, 
                "unit":sensor["unit"], 
                "recorded_at": datetime.now(timezone.utc).isoformat()
            })

            sensor_index += 1
            await asyncio.sleep(3)

    except WebSocketDisconnect:
        for device in devices:            
            device.status = "offline"
        db.commit()