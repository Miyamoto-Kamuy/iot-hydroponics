from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.device import DeviceResponse, DeviceCreate, DevicePatch
from app.services.device import get_all_devices, get_device_by_id, create_device as create_device_service, update_device as update_device_service, delete_device as delete_device_service
from app.core.deps import get_current_user, require_role
from app.models import User, Device
from typing import Literal
from datetime import datetime

router = APIRouter(prefix="/devices", tags=["devices"])

@router.get(
    "/",
    response_model=list[DeviceResponse], 
) 
def get_devices(
    user: User = Depends(get_current_user),     
    db: Session = Depends(get_db), 
    location: str | None = None,
    status: Literal["offline", "online"] | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    created_by: int | None = None,
):
    return get_all_devices(user, db, location, status, start, end, created_by)

@router.get(
    "/{id}",
    response_model=DeviceResponse, 
) 
def get_device(
    id: int,
    user: User = Depends(get_current_user),     
    db: Session = Depends(get_db)
):
    return get_device_by_id(id, user, db)

@router.post(
    "/",
    response_model=DeviceResponse
)
def create_device(
    data: DeviceCreate, 
    user: User = Depends(require_role("admin", "operator")), 
    db: Session = Depends(get_db)
):
    return create_device_service(data, user, db)

@router.patch(
    "/{id}",
    response_model=DeviceResponse
)
def update_device(
    id: int,
    data: DevicePatch, 
    user: User = Depends(require_role("admin", "operator")), 
    db: Session = Depends(get_db)
):
    return update_device_service(id, data, user, db)

@router.delete(
    "/{id}", 
    dependencies=[Depends(require_role("admin"))]
)
def delete_device(
    id: int,
    db: Session = Depends(get_db)
):
    return delete_device_service(id, db)