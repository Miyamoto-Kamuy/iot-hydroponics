from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.audit_log import AuditLogResponse
from app.services.audit_log import get_all_audit_logs, get_audit_log_by_id
from app.core.deps import get_current_user
from app.models import User
from datetime import datetime
from app.schemas.pagination import PaginateResponse

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])

@router.get(
    "", 
    response_model=PaginateResponse[AuditLogResponse]
)
def get_audit_logs(
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db), 
    action: str | None = None, 
    resource: str | None = None, 
    resource_id: int | None = None, 
    status_code: int | None = None, 
    performed_by: int | None = None, 
    start: datetime | None = None, 
    end: datetime | None = None, 
    page: int = 1, 
    size: int = 20, 
):
    return get_all_audit_logs(user, db, action, resource, resource_id, status_code, performed_by, start, end, page, size)

@router.get(
    "/{id}", 
    response_model=AuditLogResponse
)
def get_audit_log(
    id: int,
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db), 
):
    return get_audit_log_by_id(id, user, db)