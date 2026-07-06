from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.alert import AlertResponse, AlertPatch
from app.services.alert import get_all_alerts, get_alert_by_id, update_alert as update_alert_service, delete_alert as delete_alert_service
from app.core.deps import get_current_user, require_role
from app.models import User, Device, Alert
from typing import Literal
from datetime import datetime

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get(
    "/",
    response_model=list[AlertResponse]
)
def get_alerts(
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    device_id: int | None = None, 
    sensor_type: str | None = None,
    status: Literal["unread", "read", "resolved"] | None = None,
    start: datetime | None = None,
    end: datetime | None = None, 
):
    return get_all_alerts(user, db, device_id, sensor_type, status, start, end)

@router.get(
    "/{id}",
    response_model=AlertResponse
)
def get_alert(
    id: int,
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)    
):
    return get_alert_by_id(id, user, db)

@router.patch(
    "/{id}", 
    response_model=AlertResponse, 
    dependencies=[Depends(require_role("admin", "operator"))]
)
def update_device(
    id: int, 
    data: AlertPatch, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)  
):
    return update_alert_service(id, data, user, db)

@router.delete(
    "/{id}", 
    dependencies=[Depends(require_role("admin"))]
)
def delete_device(
    id: int, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db) 
):
    return delete_alert_service(id, user, db)