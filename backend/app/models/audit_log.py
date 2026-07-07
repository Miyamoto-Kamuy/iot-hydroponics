from app.database import Base
from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class AuditLog(Base):
    __tablename__= "audit_logs"
    
    id = Column(Integer, primary_key=True, nullable=False)
    action=Column(String, nullable=False)
    resource=Column(String, nullable=False)
    resource_id = Column(Integer, nullable=True)
    detail = Column(JSON, nullable=True)
    status_code = Column(Integer, nullable=False)
    error_detail = Column(String, nullable=True)
    # performed_at=Column(
    #     TIMESTAMP(timezone=True), 
    #     server_default=text('now()'), 
    #     nullable=False
    # )    
    performed_at=Column(
        TIMESTAMP(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    performed_by = Column(Integer, ForeignKey("users.id") , nullable=True)
    user=relationship(
        "User", 
        back_populates="audit_logs"
    )
