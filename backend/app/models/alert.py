from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

class Alert(Base):
    __tablename__= "alerts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    sensor_type=Column(String, nullable=False)
    message=Column(String, nullable=False)
    status=Column(String, nullable=False)        
    triggered_at=Column(
        TIMESTAMP(timezone=True), 
        server_default=text('now()'), 
        nullable=False
    )    
    device_id = Column(Integer, ForeignKey("devices.id") , nullable=False)
    device=relationship(
        "Device", 
        back_populates="alerts"
    )
