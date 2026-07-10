from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AuditLogResponse(BaseModel):
    id: int
    action: str
    resource: str
    resource_id: int | None
    detail: dict | None
    status_code: int
    error_detail: str | None
    performed_at: datetime
    performed_by: int | None
    model_config=ConfigDict(from_attributes=True)