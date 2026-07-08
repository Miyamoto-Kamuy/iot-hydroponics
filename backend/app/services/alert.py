from sqlalchemy.orm import Session
from app.core.exceptions import not_found, forbidden
from app.models import Alert, User, Device
from app.schemas.alert import AlertPatch
from datetime import datetime
from typing import Literal
from app.services.device import _get_device_or_404
from app.core.pagination import paginate

def _check_alert_access(
    device: Device, 
    user: User
):
    if user.role != "admin" and device.created_by != user.id:
        forbidden()

def _get_alert_or_404(id: int, user: User, db: Session):
    alert = db.query(Alert).filter(
        Alert.id == id
    ).first()
    if not alert:
        not_found("alert not found")
    device = _get_device_or_404(alert.device_id, db)
    _check_alert_access(device, user) 
    return alert   

def get_all_alerts(
    user: User, 
    db: Session,
    device_id: int | None = None, 
    sensor_type: str | None = None,
    status: Literal["unread", "read", "resolved"] | None = None,
    start: datetime | None = None,
    end: datetime | None = None,    
    page: int = 1, 
    size: int = 20,     
):
    query = db.query(Alert).join(Device)
    if user.role != "admin":
        query = query.filter(
            Device.created_by == user.id
        )
    if device_id:
        query = query.filter(
            Alert.device_id == device_id
        )
    if sensor_type:
        query = query.filter(
            Alert.sensor_type == sensor_type
        )
    if status:
        query = query.filter(
            Alert.status == status
        )
    if start:
        query = query.filter(
            Alert.triggered_at >= start
        )    
    if end:
        query = query.filter(
            Alert.triggered_at <= end
        )    
    return paginate(query, page, size)    

def get_alert_by_id(
    id: int, 
    user: User,
    db: Session
):    
    return _get_alert_or_404(id, user, db)

def update_alert(
    id: int,
    data: AlertPatch, 
    user: User, 
    db: Session
):
    alert = _get_alert_or_404(id, user, db)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(alert, key, value)
    db.commit()
    db.refresh(alert)
    return alert

def delete_alert(
    id: int, 
    user: User,
    db: Session
):
    alert = _get_alert_or_404(id, user, db)
    db.delete(alert)
    db.commit()

    return {"message": "alert deleted"}
