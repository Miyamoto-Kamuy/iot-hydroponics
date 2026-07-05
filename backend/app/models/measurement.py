from app.database import Base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

class Measurement(Base):
    __tablename__= "measurements"
    
    id = Column(Integer, primary_key=True, nullable=False)
    sensor_type=Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit=Column(String, nullable=False)
    recorded_at=Column(
        TIMESTAMP(timezone=True), 
        server_default=text('now()'), 
        nullable=False
    )
    
    device_id = Column(Integer, ForeignKey("devices.id") , nullable=False)
    device=relationship(
        "Device", 
        back_populates="measurements"
    )
