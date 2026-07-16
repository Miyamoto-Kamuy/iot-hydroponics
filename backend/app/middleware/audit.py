from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.models import AuditLog
from app.database import SessionLocal
from app.core.security import verify_access_token


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method not in ["POST", "PATCH", "DELETE"]:
            return await call_next(request)
        
        token = request.cookies.get("token", "")
        payload = verify_access_token(token)
        performed_by = payload.get("user_id") if payload else None

        path = request.url.path
        parts = path.strip("/").split("/")
        resource = parts[0] if parts else None
        resource_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
        
        method_to_action = {
            "POST": "CREATE", 
            "PATCH": "UPDATE", 
            "DELETE": "DELETE"
        }
        action = method_to_action.get(request.method)

        response = await call_next(request)

        status_code = response.status_code

        new_audit_log = AuditLog(
            action=action,
            resource=resource,
            resource_id = resource_id,
            detail = {"path": path, "method": request.method},
            status_code = status_code,
            error_detail = None if status_code < 300 else f"Reqeuset failed with status {status_code}",
            performed_by = performed_by
        )

        db = SessionLocal()
        try:
            db.add(new_audit_log)
            db.commit()
        finally:
            db.close()

        return response