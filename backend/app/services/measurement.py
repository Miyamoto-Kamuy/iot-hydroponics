from sqlalchemy.orm import Session
from app.core.exceptions import not_found, forbidden
from app.models import Measurement, User, Device
from datetime import datetime
from app.services.device import _get_device_or_404
from app.core.pagination import paginate

def _check_measurement_access(
    device: Device,
    user: User
):
    if user.role != "admin" and device.created_by != user.id:
        forbidden()

def get_device_measurements(    
    device_id: int,
    user: User,
    db: Session,
    sensor_type: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    page: int = 1, 
    size: int = 20, 
):
    device = _get_device_or_404(device_id, db)
    _check_measurement_access(device, user)
    query = db.query(Measurement).filter(
        Measurement.device_id == device.id
    )
    
    if sensor_type:
        query = query.filter(
            Measurement.sensor_type == sensor_type
        )    
    if start:
        query = query.filter(
            Measurement.recorded_at >= start
        )    
    if end:
        query = query.filter(
            Measurement.recorded_at <= end
        )    

    return paginate(query, page, size)

def get_all_measurements(
    user: User,
    db: Session,
    device_id: int | None = None,
    sensor_type: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    page: int = 1, 
    size: int = 20, 
):
    query = db.query(Measurement).join(Device)
    if user.role != "admin":
        query = query.filter(Device.created_by == user.id)
    if device_id:
        query = query.filter(Measurement.device_id == device_id)

    if sensor_type:
        query = query.filter(
            Measurement.sensor_type == sensor_type
        )    
    if start:
        query = query.filter(
            Measurement.recorded_at >= start
        )    
    if end:
        query = query.filter(
            Measurement.recorded_at <= end
        )    
    return paginate(query, page, size)

def get_measurement_by_id(
    id: int, 
    user: User,
    db: Session
):
    measurement = db.query(Measurement).filter(
        Measurement.id == id
    ).first()
    if not measurement:
        not_found("measure not found")
    device = _get_device_or_404(measurement.device_id, db)
    _check_measurement_access(device, user)
    return measurement