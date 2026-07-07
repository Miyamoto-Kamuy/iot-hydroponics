from sqlalchemy.orm import Session
from app.core.exceptions import not_found, forbidden
from app.models import AuditLog, User
from datetime import datetime

def _check_audit_log_access(
    user: User,
    audit: AuditLog
):
    if user.role != "admin" and audit.performed_by != user.id:
        forbidden()

def get_all_audit_logs(
    user: User, 
    db: Session, 
    action: str | None = None,
    resource: str | None = None,
    resource_id: int | None = None,  
    status_code: int | None = None,
    performed_by: int | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
): 
    query = db.query(AuditLog)
    if user.role != "admin":
        query = query.filter(AuditLog.performed_by == user.id)

    filters = {
        AuditLog.performed_by: performed_by,
        AuditLog.action: action,
        AuditLog.resource: resource,
        AuditLog.resource_id: resource_id,
        AuditLog.status_code: status_code,
    }
    for column, value in filters.items():
        if value is not None:
            query = query.filter(column == value)    
    if start:
        query = query.filter(
            AuditLog.performed_at >= start
        )    
    if end:
        query = query.filter(
            AuditLog.performed_at <= end
        )   
    return query.all()

def get_audit_log_by_id(
    id: int,
    user: User, 
    db: Session
):
    audit = db.query(AuditLog).filter(
        AuditLog.id == id
    ).first()
    if not audit:
        not_found("audit log not found")
    _check_audit_log_access(user, audit)

    return audit