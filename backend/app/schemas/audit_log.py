from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional

class AudiLogResponse(BaseModel):
    id: int
    action: str
    resource: str
    resource_id: int | None
    detail: dict | None
    status_code: int
    error_detail: str | None
    performed_at: datetime
    performed_by: int | None

    class Config:
        from_attributes = True