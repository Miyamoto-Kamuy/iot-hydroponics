from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.measurement import MeasurementResponse
from app.services.measurement import get_device_measurements, get_all_measurements, get_measurement_by_id
from app.core.deps import get_current_user, require_role
from app.models import User, Device
from datetime import datetime
from app.schemas.pagination import PaginateResponse

router = APIRouter()

@router.get(
    "/devices/{device_id}/measurements", 
    response_model=PaginateResponse[MeasurementResponse]
)
def get_measurements_with_device_id(
    device_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    sensor_type: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    page: int = 1, 
    size: int = 20, 
):
    return get_device_measurements(device_id, user, db, sensor_type, start, end, page, size)

@router.get(
    "/measurements", 
    response_model=PaginateResponse[MeasurementResponse]
)
def get_measurements(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    device_id: int | None = None,
    sensor_type: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    page: int = 1, 
    size: int = 20, 
):
    return get_all_measurements(user, db, device_id, sensor_type, start, end, page, size)

@router.get(
    "/measurements/{id}", 
    response_model=MeasurementResponse
)
def get_measurement(
    id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),    
):
    return get_measurement_by_id(id, user, db)