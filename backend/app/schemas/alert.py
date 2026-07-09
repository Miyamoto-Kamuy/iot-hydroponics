from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Literal


class AlertResponse(BaseModel):
    id: int
    sensor_type: str
    message: str
    status: str
    triggered_at: datetime
    device_id: int
    model_config=ConfigDict(from_attributes=True)
        

class AlertPatch(BaseModel):    
    status: Optional[Literal["unread", "read", "resolved"]] = None