from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Literal, Optional

class DeviceResponse(BaseModel):
    id: int
    name: str
    location: str
    status: str
    last_seen_at: datetime | None
    created_at: datetime
    created_by: int
    model_config=ConfigDict(from_attributes=True)    

class DeviceCreate(BaseModel):
    name: str
    location: str
    status: Literal["offline", "online"] = "offline"

class DevicePatch(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    status: Optional[Literal["offline", "online"]] = None