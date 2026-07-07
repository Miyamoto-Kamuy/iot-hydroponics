from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class User(Base):
    __tablename__= "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email=Column(String, nullable=False, unique=True)
    hashed_password=Column(String, nullable=False)
    role=Column(String, nullable=False)
    # created_at=Column(
    #     TIMESTAMP(timezone=True), 
    #     server_default=text('now()'), 
    #     nullable=False
    # )
    created_at=Column(
        TIMESTAMP(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    devices=relationship(
        "Device", 
        back_populates="creator"
    )
    audit_logs=relationship(
        "AuditLog", 
        back_populates="user"
    )
