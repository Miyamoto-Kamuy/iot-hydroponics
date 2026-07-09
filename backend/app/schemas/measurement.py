from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MeasurementResponse(BaseModel):
    id: int
    sensor_type: str
    value: float
    unit: str
    recorded_at: datetime
    device_id: int
    model_config=ConfigDict(from_attributes=True)