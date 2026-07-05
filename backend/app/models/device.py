from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

class Device(Base):
    __tablename__= "devices"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name=Column(String, nullable=False)
    location=Column(String, nullable=False)
    status=Column(String, nullable=False)
    last_seen_at=Column(
        TIMESTAMP(timezone=True), 
        nullable=True
    )
    created_at=Column(
        TIMESTAMP(timezone=True), 
        server_default=text('now()'), 
        nullable=False
    )
    created_by = Column(Integer, ForeignKey("users.id") , nullable=False)
    creator=relationship(
        "User", 
        back_populates="devices"
    )
    measurements=relationship(
        "Measurement", 
        back_populates="device"
    )
    alerts=relationship(
        "Alert", 
        back_populates="device"
    )
