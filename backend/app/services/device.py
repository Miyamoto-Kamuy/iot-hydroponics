from sqlalchemy.orm import Session
from app.core.exceptions import not_found, forbidden
from app.models import Device, User
from app.schemas.device import DeviceCreate, DevicePatch
from typing import Literal
from datetime import datetime
from app.core.pagination import paginate

def _get_device_or_404(
    id: int,
    db: Session
):
    device = db.query(Device).filter(Device.id == id).first()
    if not device:
        not_found("device not found")
    return device

def _check_device_owner(
    device: Device, 
    user: User
):
    if user.role != "admin" and device.created_by != user.id: 
        forbidden()


def get_all_devices(
    user: User, 
    db: Session, 
    location: str | None = None,
    status: Literal["offline", "online"] | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    created_by: int | None = None,
    page: int = 1, 
    size: int = 20, 
):
    query = db.query(Device)

    if user.role != "admin":
        query = query.filter(
            Device.created_by == user.id            
        )
    elif created_by:
        query = query.filter(
            Device.created_by == created_by
        )
    if location:
        query = query.filter(Device.location == location)
    if status:
        query = query.filter(Device.status == status)
    if start:
        query = query.filter(Device.created_at >= start)
    if end:
        query = query.filter(Device.created_at <= end)
    
    return paginate(query, page, size)

def get_device_by_id(
    id: int, 
    user: User, 
    db: Session
):    
    device = _get_device_or_404(id, db)
    _check_device_owner(device, user)
    return device

def create_device(
    data: DeviceCreate, 
    user: User, 
    db: Session
):
    new_device = Device(
        **data.model_dump(), 
        created_by = user.id
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

def update_device(
    id: int,
    data: DevicePatch, 
    user: User, 
    db: Session
):
    device = _get_device_or_404(id, db)
    _check_device_owner(device, user)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(device, key, value)
    db.commit()
    db.refresh(device)
    return device

def delete_device(
    id: int, 
    db: Session
):
    device = _get_device_or_404(id, db)    
    db.delete(device)
    db.commit()
    return {"message": "device deleted"}