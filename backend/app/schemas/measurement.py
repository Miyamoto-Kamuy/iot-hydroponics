from pydantic import BaseModel
from datetime import datetime

class MeasurementResponse(BaseModel):
    id: int
    sensor_type: str
    value: float
    unit: str
    recorded_at: datetime
    device_id: int

    class Config:
        from_attributes = True